---
name: quark-netdisk
description: "Automate Quark Drive (夸克网盘): QR-code login, list/search, upload, create share links (expiry/passcode), and save others' shared links into your drive. Use when user asks to operate Quark/夸克网盘, generate QR login, manage files under an allowlisted remote folder, create/share links, or transfer (转存) shared resources."
---

# Quark Drive automation (夸克网盘)

## Hard constraints (must follow)

- **Remote allowlist**: Only operate under remote path prefix(es) configured in `references/config.json` (or fallback `references/config.example.json`). Default allowlist should be `/OpenClaw/**`.
- **Local allowlist**: Only read/upload from local path prefix(es) configured. Do not read arbitrary local paths.
- **Destructive operations need confirmation** by default: delete / move / rename / copy / purge.
- If Quark triggers **captcha / risk control**, stop and ask the user to take over in a real browser.

## Privacy & safety (publishable skill defaults)

- Treat these files as **sensitive** (never commit, never paste their contents):
  - `references/session_api.json`, `references/cookies.json`, `references/login_token.json`, `references/qr_code.png`
  - (If enabled) `references/index.json` (may contain private filenames/paths)
- Do not print cookies, auth headers, or full raw responses unless user explicitly requests debug.
- When sharing the skill, keep examples **generic** (no usernames, absolute paths, chat_id, or personal tokens).

## Runtime / dependencies

- Runtime: **system Python** (this repo does not bundle a venv).
- Dependencies are expected to be installed by the host (often via OS packages). `requirements.txt` exists for portability/reference.

## Config

- Preferred: `references/config.json`
- Fallback: `references/config.example.json`

Key fields (example names; see `config.example.json`):
- `remoteAllowlist`: e.g. `["/OpenClaw/**"]`
- `localAllowlist`: e.g. `["/path/to/Uploads"]`
- `loginTimeoutSeconds`

## Login workflow (QR)

### Terminal (local)
1) Run `login-prepare` to generate QR
2) User scans in Quark App
3) Run `login-wait` to persist session

### Any OpenClaw channel (Telegram / WhatsApp / 飞书 ...)
Use orchestration pattern:
1) Run: `channel-run <op> ...`
2) If exit code == **10** and JSON contains `need_login: true`:
   - Send `qr_png` back to the **current chat/channel**
   - Immediately start `login-wait` (poll every ~5s)
   - When login succeeds, **automatically reply** in the same chat/channel (e.g. “登录成功”) and then re-run the original `channel-run <op> ...`

Machine-readable interaction exit codes (for orchestration):
- **10**: `need_login=true`
- **11**: `need_pick=true` (multiple candidates; re-run with `--pick`)
- **12**: `need_confirm=true` (destructive ops; re-run with `--confirm`)

## Commands (scripts/quark_drive.py)

Invoke as:
- `python3 scripts/quark_drive.py <cmd> [args...]`

### Auth
- `login`
- `login-prepare [--no-open]`
- `login-wait`
- `auth-status`
- `channel-run <op> [args...]` (preferred)
- `telegram-run <op> [args...]` (alias)

### Browse
- `mkdir <remote_path>`
- `ls <remote_path> [--json]`
- `search <keyword> [--allow-outside-openclaw]` (privacy default: scoped to `/OpenClaw/**`)

### Upload
- `upload <local_file>`

### Share (create link)

#### Conversation contract (important)
When the user asks to “生成分享链接/创建分享/分享某个文件(夹)”:
1) **Search candidates first** (do not ask user to provide full remote path).
   - Default: use server search.
   - If server search is insufficient and the user wants stronger fuzzy search, use a **client-side fuzzy index** and rank results by fuzzy score.
     - Privacy default: build the index **in-memory** (ephemeral) and do not write it to disk.
   - Only keep candidates whose resolved path is inside remote allowlist.
2) If multiple candidates: list them with **index + path + type/size**, ask user to pick.
3) Before creating the share, ask:
   - **Expiry**: 1 / 7 / 30 / 永久
   - **Passcode**: 有 / 无
     - If 有: ask for the code; if user does not provide, generate one (4–6 alnum).
4) If user does not answer: default to **no passcode + permanent**.

#### CLI
- `share-create <remote_path> [--days 1|7|30|0] [--passcode XXXX] [--title ...]`
- `share-create-auto <keyword> [--pick N] [--days 1|7|30|0] [--passcode XXXX] [--local] [--allow-outside-openclaw]`
  - If multiple candidates and `--pick` is omitted, returns JSON with `need_pick=true` and a candidate list.

Local index helpers:
- `index-build --root <remote_path> --max-items <n> [--write]` (may issue many API calls; without `--write` it does not persist)
- `search-local <keyword> [--top N]` (builds ephemeral index; does not persist)

### Share (save others' share into my drive / 转存)
- `share-save <share_text_or_url> [--passcode XXXX] [--to /OpenClaw/FromShares] [--no-wait]`

Notes:
- Quark typically **forbids saving your own share** (will error). Use an external share to test.

### Destructive
- `rename <src_path> <new_name>`
- `mv <src_path> <dst_dir>`
- `rm <src_path> --confirm` (soft-delete into `/OpenClaw/.trash`)
- `purge-trash --days <n> --confirm`

## Troubleshooting

- `auth-status` fails (401/403): session expired → run login flow again.
- `share-save` fails with “用户禁止转存自己的分享”: you tried saving your own link → test with someone else’s share.
- If endpoints change and commands start 404/410xx: capture a browser network request (copy as cURL) and update adapter.
