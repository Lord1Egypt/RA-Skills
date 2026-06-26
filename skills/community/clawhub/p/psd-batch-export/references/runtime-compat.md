# Runtime Compatibility

Use one source skill folder for Claude/ClawHub, Codex, and OpenClaw. Always resolve scripts relative to the folder that contains `SKILL.md`.

## Claude / Claude Code

Install by keeping or copying the folder under:

```powershell
~/.claude/skills/psd-batch-export
```

Run:

```powershell
python scripts/psd_batch.py diagnose --json
```

## Codex

Install by copying or syncing the same folder under:

```powershell
~/.codex/skills/psd-batch-export
```

Validate on Windows with UTF-8 mode:

```powershell
$env:PYTHONUTF8='1'
python C:\Users\26240\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\26240\.codex\skills\psd-batch-export
```

The shared `SKILL.md` intentionally avoids Claude-only frontmatter such as `argument-hint` so the same file can pass Codex validation.

## OpenClaw

Install the local folder into the shared OpenClaw managed skills directory:

```powershell
openclaw skills install "C:\Users\26240\.claude\skills\psd-batch-export" --global --force
openclaw skills check --json
```

Inspect:

```powershell
openclaw skills info psd-batch-export
```

## ClawHub

Do not publish automatically. When a release is requested, use an explicit version and changelog:

```powershell
clawhub --no-input skill publish "C:\Users\26240\.claude\skills\psd-batch-export" --slug psd-batch-export --owner luis1213899 --version 4.4.0 --changelog "v4.4.0: unified production CLI, structured reports, tests, and Claude/Codex/OpenClaw compatibility." --clawscan-note "Local PSD processing skill. Optional network access is limited to user-triggered font downloads or optional LLM calls when API keys are configured."
clawhub inspect psd-batch-export
```

Never include Git remote URLs or credentials in release notes, reports, or public logs.
