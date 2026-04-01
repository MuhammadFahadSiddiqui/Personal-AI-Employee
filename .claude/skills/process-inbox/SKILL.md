---
name: process-inbox
description: |
  Process all pending tasks in the AI Employee vault's /Needs_Action folder.
  Reads each TASK_*.md / EMAIL_*.md / FILE_*.md file, determines the required
  action per Company_Handbook.md rules, executes safe actions autonomously,
  routes sensitive actions to /Pending_Approval, then moves completed tasks
  to /Done and updates Dashboard.md.
---

# Process Inbox

Process all pending items in the AI Employee vault.

## Steps

1. **Read the handbook first**
   Read `./AI_Employee_Vault/Company_Handbook.md` to load rules of engagement.

2. **Scan /Needs_Action**
   List all `.md` files in `./AI_Employee_Vault/Needs_Action/`.
   If empty, report "Inbox clear — nothing to process." and update Dashboard.

3. **For each task file**, read the frontmatter and content, then:

   | Task type | Autonomous action |
   |-----------|-------------------|
   | `file_drop` | Summarize the dropped file; add a summary section to the task file |
   | `email` | Draft a reply; save draft to `/Pending_Approval/DRAFT_EMAIL_<id>.md` |
   | `whatsapp` | If urgent keyword → escalate to `/Pending_Approval`; else summarize |
   | `reminder` | Execute if safe (update a doc); else route to Pending_Approval |

4. **Sensitive action check** (from handbook §5):
   - Sending messages → `/Pending_Approval`
   - Payments > $100 → `/Pending_Approval`
   - Deletions → `/Pending_Approval`

5. **Mark complete**
   - Update the task file's `status:` field to `done`
   - Move the file: `./AI_Employee_Vault/Needs_Action/<file>` → `./AI_Employee_Vault/Done/<file>`

6. **Update Dashboard**
   After processing all tasks, invoke `/update-dashboard`.

7. **Log everything**
   Append each action to `./AI_Employee_Vault/Logs/activity_log.md`:
   ```
   | <ISO timestamp> | process-inbox | <event> | <detail> |
   ```

## Output

After processing, print a summary:
```
✓ Processed: N tasks
→ Moved to Done: N
→ Sent to Pending_Approval: N
⚠ Errors: N
```
