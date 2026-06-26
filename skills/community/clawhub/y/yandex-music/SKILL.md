---
name: yandex-music-control
description: Inspect Yandex Music via the MarshalX yandex-music library. Use when the user wants Yandex Music search, current track lookup, liked tracks, playlists, or a reusable helper for Yandex Music tokens.
---

# Yandex Music Control

Use the bundled helper script for deterministic operations instead of rewriting API snippets.

## First use

1. Read `references/token-and-control.md`.
2. Check whether the token is already available via `YM_TOKEN` or the workspace config file.
3. If the token is missing, ask the user for a token or guide them to provide one; do not invent an extraction flow.
4. Validate the token with:

```bash
scripts/ymctl.py auth-check
```

## Runtime

Prefer the skill-local virtualenv interpreter when present:

```bash
./.venv/bin/python scripts/ymctl.py ...
```

If `.venv` is missing, create it and install the library:

```bash
python3 -m venv .venv
./.venv/bin/pip install yandex-music
```

## Save token

```bash
./.venv/bin/python scripts/ymctl.py auth-set <TOKEN>
./.venv/bin/python scripts/ymctl.py auth-set <TOKEN> --device '<device-id>'
./.venv/bin/python scripts/ymctl.py auth-where
./.venv/bin/python scripts/ymctl.py auth-clear
```

Default config path:

```text
/root/.openclaw/workspace/.openclaw/yandex-music-control/config.json
```

## Common commands

Search tracks:

```bash
./.venv/bin/python scripts/ymctl.py search 'кино группа крови'
./.venv/bin/python scripts/ymctl.py search 'масло черного тмина' --type artist
```

Current track:

```bash
./.venv/bin/python scripts/ymctl.py now-playing
```

Likes and playlists:

```bash
./.venv/bin/python scripts/ymctl.py likes --limit 20
./.venv/bin/python scripts/ymctl.py playlists
./.venv/bin/python scripts/ymctl.py like 'shortparis страшно'
./.venv/bin/python scripts/ymctl.py unlike 'shortparis страшно'
```

## Behavior rules

- This skill is read/search oriented: do not claim live transport control.
- `now-playing` uses a local Ynison websocket probe for modern clients.
- Do not echo secrets back into chat.
- Keep token handling local to env vars or the workspace config file.

## Files

- Helper script: `scripts/ymctl.py`
- Control/token notes: `references/token-and-control.md`
