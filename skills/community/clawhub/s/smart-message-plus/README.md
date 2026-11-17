# smart-message-plus

> Cross-platform IM messaging CLI for **DingTalk (钉钉)**, **Feishu / Lark (飞书)** enterprise apps and **WeCom (企业微信)** group robot webhooks — pure Python stdlib, zero third-party dependencies.

## Features

- **Three providers, one CLI** — DingTalk, Feishu & WeCom(webhook) adapters behind a shared provider interface (Slack planned)
- **Onboarding wizard** — `--onboard` interactive setup (channel → credentials → live verify → defaults) with embedded permission checklists; `--onboard-status` shows config completeness
- **All the message types** — text, Markdown, images, files, interactive cards with jump buttons, @mentions / @all
- **Recall** — undo a sent message from the send log (DingTalk unlimited, Feishu within 24h)
- **Contact aliases** — one alias maps to per-platform user IDs; group aliases too
- **Group creation** — create chats via API (`--create-group`), auto-saved as aliases
- **Department broadcast** — resolve members via built-in contacts API or your own org-lookup HTTP service
- **Safety gate** — headcount tiers with `--force-send` warning line and single-use, content-bound admin approval codes
- **Ops-friendly** — multi-account with token cache, message templates, JSONL send log, `--dry-run` everywhere
- **Zero deps** — Python ≥ 3.9 standard library only; credentials stored 0600, atomic writes, never in git

## Quick Start

```bash
SCRIPT="python3 scripts/send.py"

# 1. Save an account (DingTalk internal app / Feishu custom app)
$SCRIPT --save-account my-dingtalk dingtalk "DT Bot" --app-key <AppKey> --app-secret <AppSecret>
$SCRIPT --save-account my-feishu feishu "FS Bot" --app-id <AppID> --app-secret <AppSecret>

# 2. Verify credentials
$SCRIPT --test-account my-dingtalk

# 3. Send
$SCRIPT --provider dingtalk --to 13800000000 --msg "hello"
$SCRIPT --provider feishu --to user@example.com --msg "hello"
$SCRIPT --chat-id my-group --msg "notice" --mention-all
```

## Install

```bash
# clawhub
clawhub install smart-message-plus

# Or clone directly
git clone https://github.com/Songhonglei/smart-message-plus.git
```

## Usage

Full documentation in [SKILL.md](./SKILL.md). References:

- [`references/provider-matrix.md`](./references/provider-matrix.md) — capability matrix & platform quirks
- [`references/console-setup.md`](./references/console-setup.md) — DingTalk / Feishu / WeCom console setup + permission checklist
- [`references/org-lookup-contract.md`](./references/org-lookup-contract.md) — custom org-lookup HTTP contract (+ mock server)

## Install in your AI agent

| Agent | Install |
|---|---|
| OpenClaw | `clawhub install smart-message-plus` |
| Claude Code | Manual: copy to `~/.claude/skills/` |
| Cursor | Manual: copy to `~/.cursor/skills/` |

## Safety notes

- **Message content must come from the user.** The CLI is a transport; AI agents must never draft outbound messages autonomously.
- Credentials live outside the skill directory (`$SMP_DATA_DIR` > `<workspace>/.smart-message/` > `~/.smart-message/`), chmod 600.
- Broadcasts above configurable thresholds require `--force-send` or an admin-issued approval code.

## License

MIT © 2026 Evan Song

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
