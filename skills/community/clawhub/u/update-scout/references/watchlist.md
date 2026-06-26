# Scout Watchlist Reference

Config file: `~/.config/scout/watchlist.json`

## Detect Types

| Type | How it works | Required fields |
|------|-------------|-----------------|
| `command` | Runs a shell command, extracts first semver from output | `cmd` (list of args) |
| `npm_global` | Runs `npm list -g <package>` | `package` |
| `pip` | Runs `pip show <package>` | `package` |
| `file` | Reads version from a JSON file | `path`, `key` (default: "version") |

## Example Entries

```json
[
  {
    "name": "openclaw",
    "repo": "openclaw/openclaw",
    "detect": {"type": "command", "cmd": ["openclaw", "--version"]},
    "version_prefix": "v",
    "notes": "Core OpenClaw runtime"
  },
  {
    "name": "my-npm-tool",
    "repo": "org/repo",
    "detect": {"type": "npm_global", "package": "my-npm-tool"},
    "version_prefix": "v",
    "notes": "Some npm tool"
  },
  {
    "name": "my-python-lib",
    "repo": "org/repo",
    "detect": {"type": "pip", "package": "my-python-lib"},
    "version_prefix": "v",
    "notes": "Some Python package"
  }
]
```

## Security Review Checklist

For every update before recommending approval:

1. **Breaking changes?** — Config schema, renamed flags, removed features
2. **Auth/network/filesystem changes?** — Extra scrutiny required
3. **Post-release regressions?** — Check GitHub issues opened after release date
4. **Impact on user's setup** — What specifically does this touch?
5. **Risk level:** 🟢 Low / 🟡 Medium / 🔴 High

## Adding Tools via CLI

```bash
python3 scripts/add_tool.py \
  --name "tool-name" \
  --repo "owner/repo" \
  --detect-type command \
  --detect-cmd "tool --version" \
  --version-prefix "v" \
  --notes "Description"
```
