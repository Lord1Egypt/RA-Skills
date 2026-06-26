---
name: slack-backup
description: 'Back up files uploaded to a Slack channel to the local doc/backup directory. Supports smart matching: multiple files, filename prefix/keyword filter, file type (pdf/video/image), and time range ("just now" = "last 5 minutes"). Trigger when the user says things like "back up the file from Slack", "back up the PDF I just sent to Slack", "save the Slack file locally", etc.'
user-invocable: true
---

# Slack Backup Skill

Backup directory: `~/.openclaw/doc/backup/`

**Strict rules (must be followed — violations are treated as critical errors):**
- **Do not** use write/edit tools to create or modify any files
- **Do not** create Python scripts, test scripts, or any auxiliary files
- **Do not** generate, guess, or fabricate file contents and write them to disk — even if the filename is known
- **Only** run `slack_backup.sh` via exec to download real files
- **Must** verify that the script outputs `SUCCESS: /path/to/file` and that the file exists with size > 0
- If the script reports `ERROR`, inform the user honestly — do not fabricate a success status

---

## Smart Matching: Interpret Intent → Set Variables → Call Script

The agent interprets the user's natural language, determines intent, sets the corresponding environment variables, then calls the script.

| User says | Environment variables |
|-----------|----------------------|
| "Back up the latest file" / "Back up this file" | (default, no variables needed) |
| "Back up the last two files" / "Back up these two files" | `LIMIT=2` |
| "Back up files starting with report" | `NAME_PREFIX=report` |
| "Back up files with contract in the name" | `NAME_CONTAINS=contract` |
| "Back up the PDF I just uploaded" / "Back up the PDF from just now" | `MINUTES=5 FILE_TYPE=pdf` |
| "Back up the video I just uploaded" | `MINUTES=5 FILE_TYPE=video` |
| "Back up the image I just uploaded" | `MINUTES=5 FILE_TYPE=image` |
| "Back up the last three files" | `LIMIT=3 MINUTES=10` |
| "Back up all PDFs from the last 5 minutes" | `MINUTES=5 FILE_TYPE=pdf LIMIT=5` |

**FILE_TYPE values**: `pdf` / `image` / `video` / `doc` / `file` (default — matches all)

---

## Invocation

```bash
# Default: back up latest file
<SKILL_DIR>/slack_backup.sh

# Back up the latest 2 files
LIMIT=2 <SKILL_DIR>/slack_backup.sh

# Back up files whose name starts with "report"
NAME_PREFIX=report <SKILL_DIR>/slack_backup.sh

# Back up PDFs uploaded in the last 5 minutes
MINUTES=5 FILE_TYPE=pdf <SKILL_DIR>/slack_backup.sh

# Back up up to 3 files from the last 10 minutes
LIMIT=3 MINUTES=10 <SKILL_DIR>/slack_backup.sh
```

Script prints `SUCCESS: /path/to/file` for each file on success.

> **Important**: The script downloads real files from the Slack API. The downloaded file size should match the original. If a backup file is unexpectedly small (e.g. a few KB), something went wrong — report the error to the user honestly.

---

## List Backups

```bash
ls -lht ~/.openclaw/doc/backup/
```
