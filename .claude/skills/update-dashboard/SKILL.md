---
name: update-dashboard
description: |
  Refresh the AI Employee's Dashboard.md with the current state of the vault.
  Counts files in each folder, lists active tasks with priorities, shows
  pending approvals, and updates the Recent Activity section from the log.
  Run after any batch of vault changes.
---

# Update Dashboard

Refresh `./AI_Employee_Vault/Dashboard.md` with live vault state.

## Steps

1. **Count files in each folder**
   - `/Inbox` — unprocessed drops
   - `/Needs_Action` — pending tasks (group by priority P0/P1/P2/P3)
   - `/Pending_Approval` — items awaiting human sign-off
   - `/Done` — tasks completed today (filter by today's date in filename)

2. **Read active tasks**
   For each file in `/Needs_Action`, read the frontmatter and extract:
   - `type`, `priority`, `status`, filename (as task name), `received`

3. **Read pending approvals**
   For each file in `/Pending_Approval`, extract `action`, `amount` (if present), `expires`.

4. **Read recent activity**
   Read the last 10 lines of `/Logs/activity_log.md`.

5. **Rewrite Dashboard.md**
   Overwrite `./AI_Employee_Vault/Dashboard.md` with this structure:

```markdown
---
last_updated: <ISO timestamp>
owner: AI Employee
type: dashboard
---

# AI Employee Dashboard

> **Status:** Active | **Last Refresh:** <timestamp>

---

## Inbox Summary
| Folder | Count |
|--------|-------|
| /Inbox (unprocessed drops) | N |
| /Needs_Action (pending tasks) | N |
| /Pending_Approval (awaiting you) | N |
| /Done (completed today) | N |

---

## Active Tasks
<table of tasks with priority, type, name, received>

---

## Pending Approvals
<list of items needing approval with action, amount, expires>

---

## Recent Activity Log
<last 10 log entries>
```

6. **Log the dashboard update**
   Append to `/Logs/activity_log.md`:
   ```
   | <timestamp> | update-dashboard | dashboard_refreshed | OK |
   ```
