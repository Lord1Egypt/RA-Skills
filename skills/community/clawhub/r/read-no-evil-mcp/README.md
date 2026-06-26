# 🦞 read-no-evil-mcp

> 🙈 *"Read no evil"* — Secure email access for your AI agent, with prompt injection protection built in.

This is an [OpenClaw](https://openclaw.ai) skill — your agent can read, send, and manage emails without you worrying about prompt injection attacks hiding in message content.

## Install

```bash
clawhub install read-no-evil-mcp
```

This skill connects to a [read-no-evil-mcp](https://github.com/thekie/read-no-evil-mcp) server. You can point it at an existing server, or let the built-in setup script spin one up locally via Docker.

## ✨ What You Get

- 📧 **Full email management** — Your agent can read, send, move, and delete emails across multiple accounts
- 🛡️ **Prompt injection protection** — Every email is scanned before your agent sees it. Malicious content gets blocked automatically
- 🔒 **Your credentials stay safe** — Passwords and email connections never touch the AI. Your agent only sees clean, sanitized content
- 🔐 **You control what your agent can do** — Read-only by default, with optional send, delete, and move permissions per account. Lock it down to specific folders if you want
- 📬 **Sender-based rules** — Set rules for known senders. Auto-trust your team, flag external contacts for confirmation, or hide noisy newsletters
- 🎛️ **Custom agent guidance** — Tell your agent how to handle emails from different senders. For example, act on messages from your team right away but ask you first about external contacts
- 🎚️ **Tune the sensitivity** — Dial detection up or down per account. Tighter for your work inbox, more relaxed for newsletters
- ✉️ **Control who your agent can email** — Restrict outgoing emails to specific people or domains
- 📎 **Attachments included** — Your agent can send emails with file attachments
- 👥 **Multiple accounts** — Connect as many email accounts as you need, each with its own permissions and rules
- 🐍 **Nothing to install** — Works out of the box with no extra dependencies

For the full feature set, head over to [read-no-evil-mcp](https://github.com/thekie/read-no-evil-mcp).

## 🔐 Security

Every email is scanned by a [DeBERTa-based ML model](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2) before reaching your agent. Scanning is never skipped, even for trusted senders. Your credentials never leave the server.

## Credits

- [read-no-evil-mcp](https://github.com/thekie/read-no-evil-mcp) — The MCP server powering secure email access
- [ProtectAI](https://protectai.com/) — Prompt injection detection model

## License

Apache 2.0 — See [LICENSE](LICENSE)
