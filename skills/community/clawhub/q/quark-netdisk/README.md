# quark-netdisk

Quark Drive (夸克网盘) automation skill for OpenClaw.

## Attribution

This project incorporates ideas and some implementation details inspired by (and adapted from) QuarkPan:
- https://github.com/lich0821/QuarkPan


Features:
- QR-code login (API-based)
- List / search / basic file ops
- Upload
- Create share links (optional passcode + expiry)
- Save (转存) others’ share links into your drive

## Quick start

Run via system Python:

```bash
python3 scripts/quark_drive.py auth-status
```

If not logged in, use the QR flow (recommended; works with OpenClaw channel orchestration):

```bash
python3 scripts/quark_drive.py login-prepare
# scan the QR with Quark app
python3 scripts/quark_drive.py login-wait
```

Terminal-only convenience (one-shot):

```bash
# This command is intended for running on a local terminal.
# It generates the QR and blocks while polling until login succeeds.
python3 scripts/quark_drive.py login
```

## Common commands

```bash
# browse
python3 scripts/quark_drive.py ls /OpenClaw
python3 scripts/quark_drive.py search 关键词  # privacy default: scoped to /OpenClaw/**
python3 scripts/quark_drive.py search 关键词 --allow-outside-openclaw

# upload (default target: /OpenClaw)
python3 scripts/quark_drive.py upload /path/to/file.zip

# create a share link (default: no passcode, permanent)
python3 scripts/quark_drive.py share-create /OpenClaw/abc

# auto-pick flow (search first; if multiple candidates, re-run with --pick)
python3 scripts/quark_drive.py share-create-auto abc
python3 scripts/quark_drive.py share-create-auto abc --pick 1 --days 7 --passcode A1B2

# save someone else’s share into your drive
python3 scripts/quark_drive.py share-save "https://pan.quark.cn/s/xxxx" --to /OpenClaw/FromShares
```

## OpenClaw channel orchestration (any channel)

Use `channel-run` to make operations login-aware:
- If logged in: runs the operation
- If not logged in: emits JSON with `need_login=true` and exits with code **10**
  - Your OpenClaw agent should send `qr_png` back to the current chat/channel,
    start `login-wait`, and automatically reply on success,
    then retry the original command.

Machine-readable interaction exit codes:
- 10: need_login
- 11: need_pick
- 12: need_confirm

```bash
python3 scripts/quark_drive.py channel-run ls /OpenClaw
```

## Privacy & safety

Sensitive runtime files (never commit / never share their contents):
- `references/session_api.json`
- `references/cookies.json`
- `references/login_token.json`
- `references/qr_code.png`
- (If enabled) `references/index.json` (may contain private filenames/paths)

## Configuration & constraints

This skill enforces strict allowlists:
- Remote allowlist (default should be `/OpenClaw/**`)
- Local allowlist (only upload/read from approved local prefixes)

See:
- `references/config.example.json`

## Dependencies

This repo does **not** bundle a virtualenv.

Required Python packages (see also `requirements.txt`):
- httpx
- httpcore
- h11
- h2
- hpack
- hyperframe
- anyio
- certifi
- idna
- typing_extensions
- qrcode
- pillow
- rich
- typer
- click
- shellingham
- markdown-it-py
- mdurl
- Pygments
- annotated-doc
