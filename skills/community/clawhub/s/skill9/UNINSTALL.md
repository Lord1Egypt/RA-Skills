# skill9 — Uninstall

Remove skill9 CLI, local skill files, hooks, and credentials from this machine.
Cloud data (backed-up skill versions) is NOT deleted.

## Before You Begin

This will remove the following. Confirm before proceeding.

| What | Path |
|------|------|
| CLI binary | `skill9` in PATH (usually `/usr/local/bin/skill9` or `~/bin/skill9`) |
| Credentials | `~/.skill9/` |
| Skill files (OpenClaw) | `~/.openclaw/skills/skill9/` |
| Skill files (Claude Code) | `~/.claude/skills/skill9/` |
| Skill files (Cursor macOS) | `~/Library/Application Support/Cursor/User/skills/skill9/` |
| Skill files (Cursor Linux) | `~/.config/Cursor/User/skills/skill9/` |
| OpenClaw AGENTS.md rule | "Skill Backup Rule (skill9)" section in `~/.openclaw/workspace/AGENTS.md` |
| Claude Code hook | `skill9 push` entry in `~/.claude/settings.json` hooks.Stop |
| Cursor hook | `skill9 push` entry in `~/.cursor/hooks.json` hooks.stop |

**Not deleted:** Your cloud skill versions remain on skill9.ai. You can restore them later with `skill9 pull --all` after reinstalling.

Tell the user what will be removed and ask: "Proceed with uninstall?"

## Step 1: Remove CLI Binary

```bash
rm "$(which skill9)"
```

## Step 2: Remove Credentials

```bash
rm -rf ~/.skill9
```

## Step 3: Remove Skill Files

Remove the skill9 skill directory from all detected platforms:

```bash
rm -rf ~/.openclaw/skills/skill9
rm -rf ~/.claude/skills/skill9
```

For Cursor, check the platform-specific path:
- macOS: `rm -rf ~/Library/Application\ Support/Cursor/User/skills/skill9`
- Linux: `rm -rf ~/.config/Cursor/User/skills/skill9`

## Step 4: Remove OpenClaw Backup Rule

Edit `~/.openclaw/workspace/AGENTS.md`: remove the entire "## Skill Backup Rule (skill9)" section (from the heading to the end of the "Do not batch." line). Do not touch other content in AGENTS.md.

## Step 5: Remove Claude Code and Cursor Hooks

### Claude Code

Edit `~/.claude/settings.json`: remove the `skill9 push` entry from `hooks.Stop` array. If the Stop array becomes empty, remove the entire Stop key. Do not touch other hook entries.

### Cursor

Edit `~/.cursor/hooks.json`: remove the `skill9 push` entry from `hooks.stop` array. If the stop array becomes empty, remove the entire stop key. Do not touch other hook entries.

## Step 6: Verify

```bash
which skill9
# Expected: no output (command not found)

ls ~/.skill9 2>/dev/null
# Expected: no such file or directory

ls ~/.openclaw/skills/skill9 2>/dev/null
# Expected: no such file or directory

grep "skill9 push" ~/.openclaw/workspace/AGENTS.md 2>/dev/null
# Expected: no output
```

## Done

skill9 has been fully removed from this machine. Cloud data is preserved — reinstall anytime with:

```bash
curl -fsSL https://skill9.ai/install.sh | sh
```
