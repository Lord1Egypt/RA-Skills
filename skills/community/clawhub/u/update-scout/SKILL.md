---
name: scout
description: "Automate update tracking for OpenClaw and any other GitHub-released tools. Scout monitors your watchlist weekly, reviews release notes with a security lens, checks for post-release regressions, and posts a recommendation card before asking for approval — so you always know what changed and why before anything gets installed. Use when checking for available updates, reviewing a release link, running a periodic software health check, or adding new tools to monitor. Never installs anything without explicit approval."
---

# Scout — Software Update Advisor

Scout monitors GitHub releases for watched tools, reviews release notes, assesses risk, and recommends whether to upgrade. It never installs anything without explicit approval.

## Running a Check

```bash
python3 scripts/check_updates.py
# structured output:
python3 scripts/check_updates.py --json
```

Config is read from `~/.config/scout/watchlist.json`. Created automatically on first run with openclaw as the default.

## Adding a Tool (conversational)

When a user wants to add a tool, ask for:
1. GitHub repo (e.g. `owner/repo`)
2. How to detect the installed version (command, npm, pip, or file)

Then run:
```bash
python3 scripts/add_tool.py \
  --name "tool-name" \
  --repo "owner/repo" \
  --detect-type command \
  --detect-cmd "tool --version" \
  --version-prefix "v" \
  --notes "What this tool does"
```

See `references/watchlist.md` for supported detect types and examples.

## Verifying a Release

Before recommending any upgrade, run the issue checker:

```bash
python3 scripts/verify_release.py --repo owner/repo --since YYYY-MM-DD
```

Reports bug-labeled issues and regression keywords created after the release date.

## Skipping a Version

When a user decides to skip an update:

```bash
python3 scripts/skip_release.py --tool toolname --version v1.2.3 --reason "why"
# list skipped:
python3 scripts/skip_release.py --list
# un-skip:
python3 scripts/skip_release.py --clear --tool toolname
```

Skipped versions are stored in `~/.config/scout/skip_list.json` and suppressed from future `check_updates.py` output.

## Review Workflow

For every update found, produce a full recommendation card before asking for approval:

```
🔔 Update: <tool name> <installed> → <latest>
   Source: <GitHub repo> by <author/org>
   Released: <date>

Risk: 🟢/🟡/🔴 <level>

What changed:
- <plain-language summary>
- <note security fixes, breaking changes, new permissions>

Impact on our setup:
- <what this touches in config/workflow>
- <anything requiring config changes or re-auth>

Post-release issues: <none found / list any regressions>

Recommendation: <Upgrade now / Wait / Skip>
Reason: <one sentence>
```

Never ask "want me to upgrade X?" without the full card. The user needs enough context to decide without prior knowledge of the tool.

**Risk levels:**
- 🟢 Low — patch/fix only, no config changes, no new permissions
- 🟡 Medium — new features, minor config additions, optional breaking changes
- 🔴 High — breaking changes, auth changes, schema migrations, security patches

## After Approval

1. Run the appropriate install command for the tool
2. Validate config if applicable (`openclaw config validate`)
3. Restart services if needed
4. Confirm health

## Skill Health Review

Periodically review your own skills against OpenClaw best practices:

```bash
python3 scripts/review_skills.py [--skills-dir /path/to/skills]
```

Checks each skill for structural issues and quality improvements. Reports findings — all changes require explicit approval before applying.

## Periodic Use

Add to heartbeat or weekly cron. Recommended cadence: weekly (Sundays).
