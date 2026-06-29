# rename-session

Minimal, zero-dependency tool to rename a session label in OpenClaw-style
`sessions.json`. Random label generator (zh/en), multi-agent auto-detection,
list mode, retry-with-verification, and XDG-compliant history storage.

## Why

OpenClaw and several agent runtimes store session metadata as
`<agents-root>/<agent>/sessions/sessions.json` keyed by session id, with a
`label` field shown in the UI. Editing this directly is the fastest way to
rename a session without going through any UI.

## Install

```bash
git clone https://github.com/Songhonglei/better-agent-skills.git
cd better-agent-skills/skills/rename-session
python3 scripts/rename_session.py --help
```

Or with the `skills.sh` CLI:

```bash
npx skills add Songhonglei/better-agent-skills -s rename-session
```

Or with `clawhub`:

```bash
clawhub install rename-session
```

## Quick start

```bash
# List sessions (auto-detects the only agent under ~/.openclaw/agents/)
python3 scripts/rename_session.py --list

# Rename a session with a literal label
python3 scripts/rename_session.py agent:main:main "My new session name"

# Random label (auto-detect zh/en from $LANG)
python3 scripts/rename_session.py agent:main:main --random

# Force Chinese
python3 scripts/rename_session.py agent:main:main --random --lang zh

# Force English
python3 scripts/rename_session.py agent:main:main --random --lang en
```

## Configuration

Two environment variables are supported, both optional:

| Env var | Purpose | Default |
|---|---|---|
| `RENAME_SESSION_ROOT` | Override agents root directory | `~/.openclaw/agents` |
| `XDG_DATA_HOME` | Where label history is stored | `~/.local/share` |

History file lives at `$XDG_DATA_HOME/rename-session/history.json` and keeps
the last 10 generated labels (so `--random` does not immediately repeat).

## Exit codes

- `0` - success
- `1` - failure (file missing, permission, retries exhausted)
- `2` - bad CLI arguments

## License

MIT - see [LICENSE](LICENSE).

## Author

Evan Song <songhonglei1985@gmail.com> -
[github.com/Songhonglei](https://github.com/Songhonglei)
