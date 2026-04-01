"""
filesystem_watcher.py - Monitors the vault /Inbox folder for new files.

When a file is dropped into /Inbox, this watcher:
1. Copies it to /Needs_Action
2. Creates a companion .md action file with metadata
3. Logs the event

Usage:
    python filesystem_watcher.py --vault /path/to/AI_Employee_Vault

Dependencies:
    uv add watchdog
"""
import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

sys.path.insert(0, str(Path(__file__).parent))
from base_watcher import BaseWatcher, logging

logger = logging.getLogger("FilesystemWatcher")


class DropFolderHandler(FileSystemEventHandler):
    """Handles new files dropped into /Inbox."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / "Inbox"
        self.needs_action = self.vault_path / "Needs_Action"
        self.logs = self.vault_path / "Logs"
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        # Ignore hidden/temp files
        if source.name.startswith(".") or source.suffix in (".tmp", ".part"):
            return
        self._process_file(source)

    def _process_file(self, source: Path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_name = f"FILE_{timestamp}_{source.name}"
        dest = self.needs_action / dest_name

        # Copy the file
        shutil.copy2(source, dest)
        logger.info(f"Copied {source.name} → {dest_name}")

        # Create metadata action file
        meta_path = self.needs_action / f"TASK_{timestamp}_{source.stem}.md"
        self._create_metadata(source, dest, meta_path)
        logger.info(f"Created action file: {meta_path.name}")

        # Log the event
        self._log_event(source.name, meta_path.name)

    def _create_metadata(self, source: Path, dest: Path, meta_path: Path):
        now = datetime.now().isoformat(timespec="seconds")
        content = f"""---
type: file_drop
original_name: {source.name}
file_copy: {dest.name}
size_bytes: {source.stat().st_size}
received: {now}
priority: P2
status: pending
---

# New File Dropped: {source.name}

A new file was dropped into the Inbox and is ready for processing.

## File Details
- **Original name:** `{source.name}`
- **Copied to:** `{dest.name}`
- **Size:** {source.stat().st_size:,} bytes
- **Received:** {now}

## Suggested Actions
- [ ] Open and review the file content
- [ ] Determine required action (reply, process, archive)
- [ ] Update this file with action taken
- [ ] Move to `/Done` when complete

## Notes
_Add any context or instructions here._
"""
        meta_path.write_text(content, encoding="utf-8")

    def _log_event(self, filename: str, action_file: str):
        log_file = self.logs / "activity_log.md"
        timestamp = datetime.now().isoformat(timespec="seconds")
        entry = f"| {timestamp} | FilesystemWatcher | file_dropped | {filename} → {action_file} |\n"
        with log_file.open("a", encoding="utf-8") as f:
            if log_file.stat().st_size == 0:
                f.write("# Activity Log\n\n| Timestamp | Source | Event | Detail |\n|-----------|--------|-------|--------|\n")
            f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="AI Employee — File System Watcher")
    parser.add_argument(
        "--vault",
        default=str(Path(__file__).parent.parent / "AI_Employee_Vault"),
        help="Path to the AI_Employee_Vault directory",
    )
    args = parser.parse_args()

    vault_path = Path(args.vault).resolve()
    inbox = vault_path / "Inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    logger.info(f"Vault: {vault_path}")
    logger.info(f"Watching: {inbox}")
    logger.info("Drop files into /Inbox to trigger processing. Press Ctrl+C to stop.")

    handler = DropFolderHandler(str(vault_path))
    observer = Observer()
    observer.schedule(handler, str(inbox), recursive=False)
    observer.start()

    try:
        while observer.is_alive():
            observer.join(timeout=1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()
    observer.join()
    logger.info("Watcher stopped.")


if __name__ == "__main__":
    main()
