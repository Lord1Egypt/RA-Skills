# skill9 — Setup

## First-Time Setup

Run these checks once. Do not repeat if already set up.

1. **Install CLI** (skip if `skill9` is already in PATH):
   ```bash
   npm install -g skill9
   ```

2. **Login** (skip if `skill9 whoami --json` succeeds):
   ```bash
   skill9 login --github
   ```
   Tell the user: "Please open the URL and click Authorize."

3. **Initial backup**:
   ```bash
   skill9 push --all --json
   ```

## Auto-Backup Rules

After performing ANY of the following actions on skills, you MUST immediately run the corresponding command:

| Action | Command |
|--------|---------|
| Created a new skill | `skill9 push <skill-name> --json` |
| Edited any skill file | `skill9 push <skill-name> --json` |
| Downloaded/installed a skill | `skill9 push <skill-name> --json` |
| Deleted a skill | `skill9 push --delete <skill-name> --json` |

Do not batch — push after EACH individual operation.

If push returns `"unchanged": true`, that is normal. Not an error.

## Supported Platforms

| Platform | Skills Directory |
|----------|-----------------|
| Claude Code | `~/.claude/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| Cursor (macOS) | `~/Library/Application Support/Cursor/User/skills/` |
| Cursor (Linux) | `~/.config/Cursor/User/skills/` |
| Cursor (Windows) | `%APPDATA%/Cursor/User/skills/` |
