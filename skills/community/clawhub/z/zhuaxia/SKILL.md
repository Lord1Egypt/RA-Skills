---
name: zhuaxia
description: "Export and import OpenClaw instances as portable .claw packages for backup, sharing, and migration. Use when: user wants to back up, share, migrate, or restore their OpenClaw setup. Triggers: 'export claw', 'save my setup', 'backup my instance', 'import claw', 'load this claw', 'install this claw package', 'migrate openclaw', 'rollback', 'undo import'."
metadata:
  {
    "openclaw":
      {
        "emoji": "🦐",
        "requires": { "bins": ["node"] },
      },
  }
---

# Zhuaxia (抓虾) — OpenClaw Instance Export/Import

Export and import entire OpenClaw instances as portable `.claw` packages. Sensitive data (API keys, tokens) is automatically stripped. Auto-backup before import, with rollback support.

## CLI Reference

### Save (Export)

```bash
node {baseDir}/scripts/clawctl.mjs save <namespace/name:tag> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-o <path>` | Output file path | `./<name>-<tag>.claw` |
| `--source <path>` | OpenClaw state directory | `~/.openclaw` |
| `--description <text>` | Package description | (empty) |
| `--include-memory` | Include MEMORY.md | false |

### Load (Import)

```bash
node {baseDir}/scripts/clawctl.mjs load <file> [options]
```

Load **automatically creates a backup** before installing. This can be skipped with `--no-backup`.

| Flag | Description | Default |
|------|-------------|---------|
| `--target <path>` | Target OpenClaw state dir | `~/.openclaw` |
| `--agent-name <name>` | Name for the imported agent | from manifest |
| `--dry-run` | Preview without installing | false |
| `--no-backup` | Skip auto-backup | false |

### Backup

```bash
node {baseDir}/scripts/clawctl.mjs backup [--source <path>] [--label <text>]
```

Create a snapshot of current workspace + config. Stored in `~/.openclaw/.zhuaxia-backups/<id>/`.

### List Backups

```bash
node {baseDir}/scripts/clawctl.mjs backups [--source <path>]
```

### Rollback

```bash
node {baseDir}/scripts/clawctl.mjs rollback [<id>] [--target <path>]
```

Restore from a backup. If no `<id>` given, uses the latest. Before restoring, a safety backup of the current state is created automatically.

---

## AI Agent Behavior Guide

When the user triggers this skill, follow the intelligent workflows below instead of blindly running commands.

### Export Workflow

When the user says things like "导出 claw", "export my setup", "backup my openclaw":

**Step 1 — Gather context automatically**

Before asking the user anything, silently gather:

```bash
# Check what's in the workspace
ls ~/.openclaw/workspace/

# Read identity to infer a good package name
cat ~/.openclaw/workspace/IDENTITY.md 2>/dev/null | head -20

# Check installed skills (these get recorded in the manifest)
clawhub list --workdir ~/.openclaw 2>/dev/null

# Check config exists
test -f ~/.openclaw/openclaw.json && echo "config exists" || echo "no config"
```

**Step 2 — Infer smart defaults, then confirm with user**

Based on what you found:
- **ref**: Use the agent's name/identity as the package name. Example: if IDENTITY.md says the agent is called "X", use `user/x:v1`. If unclear, ask.
- **output**: Default to `~/Desktop/<name>.claw` (easy to find and share). On Linux, use `~/`.
- **description**: Summarize the agent's personality/purpose from IDENTITY.md or SOUL.md in one sentence.
- **include-memory**: Default NO. Only suggest YES if the user explicitly mentions wanting to transfer memories.

Present your plan concisely:

> I'll export your OpenClaw as `user/x:v1` to `~/Desktop/x-v1.claw`.
> Description: "An assistant named X with ..."
> Memory: not included
> Skills bundled: zhuaxia@0.3.0, custom-skill (2 skills from ~/.openclaw/skills/)
>
> Proceed?

**Step 3 — Execute and report**

```bash
node {baseDir}/scripts/clawctl.mjs save <ref> -o <path> --description "<desc>"
```

After success, tell the user:
1. The file location and size
2. How many files were included
3. How many credentials were stripped (reassure them it's safe to share)
4. How to transfer it: "Copy this file to another machine, then tell that machine's OpenClaw '请安装这个 claw 包'"

### Import Workflow

When the user says things like "导入 claw", "install this claw", "load this package", or provides a `.claw` file path:

**Step 1 — Locate the .claw file**

If the user didn't specify a path, search for it:

```bash
# Check common locations
ls ~/Desktop/*.claw ~/Downloads/*.claw /tmp/*.claw ~/*.claw 2>/dev/null
```

If multiple `.claw` files found, list them and ask which one. If none found, ask the user for the path.

**Step 2 — Preview first (always)**

ALWAYS dry-run before installing:

```bash
node {baseDir}/scripts/clawctl.mjs load <file> --dry-run
```

Present the preview to the user clearly:
- Package name and description
- Number of workspace files (list them)
- Required credentials that need to be configured
- Required skills that need to be installed

**Step 3 — Analyze conflicts**

Before installing, check what already exists:

```bash
# Check if workspace files would be overwritten
ls ~/.openclaw/workspace/
```

If existing files would be overwritten, WARN the user explicitly:

> The following files already exist and will be overwritten:
> - IDENTITY.md
> - SOUL.md
>
> Your current agent personality will be replaced. A backup will be created automatically so you can rollback if needed. Continue?

**Step 4 — Install (with auto-backup)**

The load command automatically creates a backup before installing:

```bash
node {baseDir}/scripts/clawctl.mjs load <file>
```

This will output something like:
```
  Creating backup before install...
  Backup created: 20260308-143022 (12 files)
  Rollback with: clawctl rollback 20260308-143022
```

Tell the user the backup id and reassure them they can rollback at any time.

**Step 5 — Post-install intelligence**

This is where AI adds the most value. The `load` command already handles:
- Auto-backup before install (with rollback id)
- Workspace file installation
- **Bundled skill installation** (skills packaged in the .claw are auto-installed to `~/.openclaw/skills/`)
- Existing skill version comparison (skips if same or newer version already installed)

After the load command completes, the agent should handle:

1. **Skill gap check** — The load output shows "Additional skills referenced in config (not bundled, may be built-in)". For each:
   - If it's a built-in OpenClaw skill (like `coding-agent`, `github`), it's already available — no action needed.
   - If it's a ClawHub skill, offer to install:

   ```bash
   clawhub install <skill-name> --workdir ~/.openclaw
   ```

2. **Config merge** — Read both `~/.openclaw/openclaw.json` and `~/.openclaw/openclaw.imported.json`. Identify what the imported config adds (new model providers, channel settings, skill configurations) vs what the current config already has. Present a summary:

   > The imported config includes:
   > - Telegram channel config (needs bot token)
   > - Custom model provider "kimi-code"
   > - Skill config for "nano-banana-pro"
   >
   > Your current config already has: [list]
   > New items to merge: [list]
   > Shall I merge the non-sensitive settings?

   If the user agrees, read both JSON files, merge intelligently (keep current credentials, add new non-sensitive settings), and write back to `openclaw.json`.

3. **Credential checklist** — For each `$CLAW_PLACEHOLDER` in the imported config, tell the user exactly what they need to set:

   > To complete the setup, you need to configure:
   > - Telegram bot token: `openclaw config set channels.telegram.botToken <your-token>`
   > - Gateway auth token: `openclaw config set gateway.auth.token <your-token>`

4. **Verification** — After everything is done, do a quick health check:

   ```bash
   # Verify workspace files are in place
   ls ~/.openclaw/workspace/
   # Verify skills are installed
   ls ~/.openclaw/skills/
   # Verify config is valid JSON
   node -e "JSON.parse(require('fs').readFileSync(require('os').homedir()+'/.openclaw/openclaw.json','utf8')); console.log('Config OK')"
   ```

### Rollback Workflow

When the user says "回滚", "rollback", "undo import", "restore my old config":

**Step 1 — List available backups**

```bash
node {baseDir}/scripts/clawctl.mjs backups
```

Show the user what's available with timestamps and labels.

**Step 2 — Confirm which backup to restore**

If only one backup exists, confirm:

> Found 1 backup: `20260308-143022` (before-load:my-bot.claw, 12 files)
> Restore this? A safety backup of your current state will be created first.

If multiple, ask user to pick.

**Step 3 — Execute rollback**

```bash
node {baseDir}/scripts/clawctl.mjs rollback <id>
```

The rollback command automatically creates a safety backup of the current state before restoring, so the user can undo the undo if needed.

**Step 4 — Verify**

```bash
ls ~/.openclaw/workspace/
```

Confirm the restored files match expectations.

### Manual Backup Workflow

When the user says "备份一下当前状态", "save a checkpoint", "backup before I try something":

```bash
node {baseDir}/scripts/clawctl.mjs backup --label "user description here"
```

Report the backup id so they can reference it later.

### Edge Cases

- **User says "导出" without any context**: Gather info first, then propose defaults. Never ask more than 2 questions.
- **User provides a URL instead of a file path**: Download the file first with `curl -o /tmp/downloaded.claw <url>`, then proceed with import.
- **Import on a fresh OpenClaw with no existing config**: Skip conflict checking, just install everything directly. Auto-backup still runs (backs up the empty state — gives a clean rollback target).
- **User wants to export + share in one step**: After export, suggest easy transfer methods (AirDrop, scp, cloud drive).
- **Multiple .claw files**: If the user says "install all claw packages", iterate through them one by one with preview for each.
- **Rollback chain**: Each rollback creates a safety backup, so the user can always undo a rollback. Explain this when asked.
- **Disk space**: If the user has many backups, suggest cleaning old ones: `rm -rf ~/.openclaw/.zhuaxia-backups/<old-id>`.

## What Gets Exported

- Workspace files (system prompt, agent personality, custom instructions)
- Sanitized configuration (credentials replaced with `$CLAW_PLACEHOLDER`)
- **All user-installed skills** from `~/.openclaw/skills/` (full files, auto-installed on import)
- Skill list and channel list (metadata for dependency tracking)

## What Does NOT Get Exported

- API keys, tokens, passwords (automatically stripped)
- Session logs and history
- Memory (unless `--include-memory` is specified)
- Credentials directory
- Binary files (images, keys, certificates)

## What Gets Backed Up (on load/rollback)

- All workspace files (`~/.openclaw/workspace/`)
- Configuration (`~/.openclaw/openclaw.json`)
- Stored in `~/.openclaw/.zhuaxia-backups/<timestamp>/`
