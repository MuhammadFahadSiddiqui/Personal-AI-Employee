"""base_watcher.py - Abstract base class for all AI Employee watchers."""
import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class BaseWatcher(ABC):
    """Base class all watchers inherit from."""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / "Needs_Action"
        self.logs = self.vault_path / "Logs"
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        self._ensure_folders()

    def _ensure_folders(self):
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)

    def _log_event(self, event: str, detail: str = ""):
        log_file = self.logs / "activity_log.md"
        timestamp = datetime.now().isoformat(timespec="seconds")
        entry = f"| {timestamp} | {self.__class__.__name__} | {event} | {detail} |\n"
        with log_file.open("a") as f:
            if log_file.stat().st_size == 0:
                f.write("# Activity Log\n\n| Timestamp | Source | Event | Detail |\n|-----------|--------|-------|--------|\n")
            f.write(entry)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process."""

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in Needs_Action folder."""

    def run(self):
        self.logger.info(f"Starting {self.__class__.__name__} — watching every {self.check_interval}s")
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    path = self.create_action_file(item)
                    self.logger.info(f"Created action file: {path.name}")
                    self._log_event("action_file_created", path.name)
            except KeyboardInterrupt:
                self.logger.info("Watcher stopped by user.")
                break
            except Exception as e:
                self.logger.error(f"Error in watch loop: {e}")
                self._log_event("error", str(e))
            time.sleep(self.check_interval)
