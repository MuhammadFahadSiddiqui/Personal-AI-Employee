# Personal AI Employee — Claude Code Context

## Project Overview
This is a Personal AI Employee built for the Governor Sindh IT Initiative Hackathon.
The AI Employee manages personal and business affairs autonomously using Claude Code + Obsidian vault.

## Vault Location
All data lives in: `./AI_Employee_Vault/`

## Folder Structure
```
AI_Employee_Vault/
├── Dashboard.md          ← Real-time status summary (update after every run)
├── Company_Handbook.md   ← Rules of engagement — READ THIS FIRST
├── Business_Goals.md     ← Targets and KPIs (create if missing)
├── Inbox/                ← Drop zone: new files trigger the watcher
├── Needs_Action/         ← Tasks pending processing (TASK_*.md files)
├── Done/                 ← Completed tasks (move here when done)
├── Pending_Approval/     ← Sensitive actions awaiting human sign-off
├── Briefings/            ← Generated CEO briefings and reports
└── Logs/
    └── activity_log.md   ← Audit trail of all agent actions
```

## Operating Rules
1. **Always read `Company_Handbook.md` before taking any action.**
2. **Always update `Dashboard.md`** at the end of every run.
3. **Never send messages, make payments, or post to social media directly** — write to `/Pending_Approval` first.
4. **Move task files to `/Done`** after completing them (don't delete).
5. **Log every action** to `/Logs/activity_log.md`.

## Task File Format
Action files in `/Needs_Action` follow this naming pattern:
- `TASK_<YYYYMMDD_HHMMSS>_<description>.md`
- `EMAIL_<id>.md`
- `FILE_<YYYYMMDD_HHMMSS>_<filename>.md`

Each has YAML frontmatter with `type`, `status`, `priority`, and `received` fields.

## Workflow Pattern
```
Read Handbook → Scan /Needs_Action → Process each task →
Write outputs → Update /Done → Update Dashboard.md → Log activity
```

## Priority Levels
- P0 🔴 Critical — act immediately
- P1 🟠 High — within 1 hour
- P2 🟡 Medium — within 24 hours
- P3 🟢 Low — next batch

## Available Skills
- `/process-inbox` — Process all pending tasks in /Needs_Action
- `/update-dashboard` — Refresh Dashboard.md with current vault state
