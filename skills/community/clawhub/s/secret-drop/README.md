# openclaw-secret-drop

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-green.svg)](pyproject.toml)
[![OpenClaw: 2026.8+](https://img.shields.io/badge/OpenClaw-Compatible-orange.svg)](SKILL.md)

**Zero-trace secret ingest for OpenClaw messenger agents.**

Feed API keys, database URLs, and passwords to and from OpenClaw bots over Telegram, Discord, or Slack via single-use self-destructing links. Plaintext never enters chat transcripts, process logs, command arguments, or model context.

---

## The Problem

In recent OpenClaw versions (2026.8+ and 2026.9+):

1. **Mandatory Redaction:** The runtime's `tools`-mode redaction is permanently enabled. If you paste an API key or password into chat, OpenClaw irrevocably masks it (e.g. `sk-or-...` becomes `***` or `sk-or-…4a2b`) before committing the turn to SQLite transcript storage. Subsequent tool runs and replayed turns only receive the corrupted mask.
2. **Unavailable Secret Prompts on Messenger-Only Setups:** OpenClaw's official `secrets` tool uses a masked Control UI or native-app prompt. On headless servers, VPS nodes, or bots running strictly via Telegram/Discord without a usable public Control UI origin, that supported prompt may be unavailable.

## The Solution: `secret-drop`

Instead of sending plaintext over chat:

```
[Operator] ──(pastes key)──> [Password Pusher / SnapPwd]
                                        │
                                  (1-time link)
                                        │
[Telegram / Discord] ───────────────────┼──────────> [OpenClaw Agent]
                                        │                   │
                                        │            (silent CLI ingest)
                                        ▼                   ▼
                                 [Link Burned]       ~/.openclaw/.env
                                                    (atomic mode 0600)
```

1. You create an expiring single-use link on an established secret sharing service.
2. You send only the retrieval-step link to your agent in chat: `"Set OPENROUTER_API_KEY from https://eu.pwpush.com/p/abc12345/r"`.
3. The agent invokes `secret-drop`.
4. The CLI fetches the secret in-process and writes it atomically to the desired target (`~/.openclaw/.env`, local `.env`, or OpenClaw SQLite secret store). A provider configured for one retrieval consumes or expires the drop.
5. The CLI outputs only a safe confirmation (`Stored 64 bytes as OPENROUTER_API_KEY`). **The secret never touches standard output or chat history.**

---

## Supported Services

| Service | Encryption | Transport | Zero-Knowledge | Setup Required |
|---|---|---|---|---|
| **[Password Pusher](https://pwpush.com)** | AES-GCM (server) | Native JSON API | No (server decrypts) | None (public instance or self-hosted) |
| **[SnapPwd](https://snappwd.io)** | AES-GCM (client) | Native AES-GCM decrypt | **Yes** (key in `#` fragment) | Python `cryptography` (installed by this package) |

*Note:* Password Pusher and SnapPwd run entirely in-process using native HTTPS and WebCrypto-compatible AES-GCM decryption. They do not spawn helper processes or expose decryption keys on command-line arguments.

---

## Supported Destinations

1. **`openclaw-env`** (Default for providers):
   Writes directly into `~/.openclaw/.env` (or `$OPENCLAW_STATE_DIR/.env`). Atomic write, permissions enforced to `0600`. Perfect for `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, etc.
2. **`openclaw-store`**:
   Feeds the secret directly into OpenClaw's SQLite team secret store via `openclaw secrets store set <NAME> --kind secret`. Supports optional `--allow-host` for proxy egress and `--config-path` binding.
3. **`dotenv`**:
   Appends or updates a specific `.env` file in an application workspace.
4. **`file`**:
   Writes a standalone mode `0600` secret file (e.g. for service account JSON or PEM certificates).

---

## Installation

### As an OpenClaw Skill (Recommended)

Add this repository as an `extraDirs` source in your OpenClaw configuration:

```bash
git clone https://github.com/sprintberlin/openclaw-secret-drop.git ~/github_repos/openclaw-secret-drop
```

In `~/.openclaw/openclaw.json`:
```json5
{
  skills: {
    load: {
      extraDirs: [
        "~/github_repos/openclaw-secret-drop"
      ]
    }
  }
}
```

Then reload or restart your gateway.

### Standalone CLI

```bash
git clone https://github.com/sprintberlin/openclaw-secret-drop.git
cd openclaw-secret-drop
pip install -r requirements.txt
sudo ln -s $(pwd)/scripts/secret-drop /usr/local/bin/secret-drop
```

---

## CLI Usage

### Ingest from Password Pusher to OpenClaw global env:
```bash
secret-drop ingest "https://eu.pwpush.com/p/kngc42l6azicpqj5hbu/r" \
  --to openclaw-env \
  --name "OPENROUTER_API_KEY" \
  --restart-gateway \
  --json
```

For messenger delivery, enable Password Pusher's retrieval step and preserve the
generated `/r` suffix. If creating a push through `POST /p.json`, forward the exact
`html_url` response field. Do not reconstruct `https://pwpush.com/p/<token>`:
that bare route reveals and consumes the secret on a GET, including a Telegram
link-preview request.

`--restart-gateway` is optional and only acts when the selected destination reports
`restart_required: true`. It runs `openclaw gateway restart --safe`, so OpenClaw can
defer the restart until active work has drained. Without the flag, Secret Drop stores
the value and leaves `restart_required: true` in the result.

### Ingest from SnapPwd (Client-Side Encrypted):
```bash
secret-drop ingest "https://snappwd.io/g/sp-uuid123#base58key" \
  --to openclaw-env \
  --name "OPENROUTER_API_KEY" \
  --json
```

### Share a stored secret outbound to an operator:
```bash
secret-drop share \
  --from openclaw-env \
  --name "OPENROUTER_API_KEY" \
  --json
```

### Output:
```json
{
  "bytes": 64,
  "created": false,
  "destination": "openclaw-env",
  "name": "OPENROUTER_API_KEY",
  "ok": true,
    "path": "/home/alice/.openclaw/.env",
  "provider": "pwpush",
  "replaced": true,
  "gateway_restarted": true,
  "restart_required": false
}
```

Share output:
```json
{
  "expire_days": 1,
  "expire_views": 1,
  "ok": true,
  "provider": "pwpush",
  "retrieval_step": true,
  "url": "https://pwpush.com/p/abcdef123456/r"
}
```

---

## Security Guarantees

- **No Output Leakage:** The CLI strictly suppresses secrets on `stdout`, `stderr`, and exit codes.
- **Atomic File Writes:** Writes use temporary files in the target directory, `fchmod 0600`, `fsync`, and atomic `os.replace`. The destination is checked again with `lstat` immediately before replacement to reject a late symlink swap.
- **SSRF Guardrails:** The HTTP client requires HTTPS, rejects URL userinfo, validates every redirect, and rejects the request if any resolved A/AAAA result is private, loopback, link-local, multicast, reserved, unspecified, or scoped. Self-hosted private instances require explicit `--allow-private-host`. This is defense in depth, not a replacement for host network policy.
- **URL Redaction:** Provider identifiers in `/p/<token>` and `/g/<id>` paths, query strings, and fragments are masked in status and error output.
- **No false erase promise:** Python cannot guarantee erasure of immutable strings or SSD/journal history. The design minimizes copies and never emits plaintext; use a protected OpenClaw store or external secret manager when stronger storage isolation is required.

---

## License

MIT License. Developed by SprintCX.
