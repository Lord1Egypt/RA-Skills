# TRTC AI Customer Service Skill

English | [简体中文](README_ZH.md)

> Rapidly scaffold a production-ready AI customer service Web application powered by [Tencent RTC Conversational AI](https://trtc.io/solutions/conversational-ai) — voice & text dual-mode, trilingual, with built-in e-commerce workflows.

## Highlights

| Capability | Description |
|-----------|-------------|
| **Real-time Voice** | Bidirectional WebRTC audio between end-user and cloud-hosted AI Bot |
| **Text Fallback** | Bypass ASR — send typed messages directly to the LLM pipeline |
| **Trilingual i18n** | Chinese / Cantonese / English across UI, STT, TTS, and SystemPrompt |
| **E-commerce Workflows** | Order inquiry, returns & exchanges, shipping tracking, promotions |
| **Digital Avatar** | Optional virtual human rendering; graceful degradation to pure voice |
| **Session Lifecycle** | Keyword-triggered farewell, human agent transfer, auto-idle timeout |
| **Service Rating** | 4-dimension post-session evaluation |

## Installation

This is a **portable Agent Skill** (a `SKILL.md` + `scripts/` + `references/` + `assets/` bundle). Install it to your tool's skills directory and the agent will auto-discover it.

### OpenClaw

Choose the install location based on your needs:

| Location | Scope | Command |
|----------|-------|---------|
| `<workspace>/skills/` | Current workspace, highest priority | `git clone https://github.com/jerryang-cool/trtc-ai-customer-service-skill.git skills/trtc-ai-customer-service` |
| `~/.agents/skills/` | Personal, effective across workspaces | `git clone https://github.com/jerryang-cool/trtc-ai-customer-service-skill.git ~/.agents/skills/trtc-ai-customer-service` |
| `~/.openclaw/skills/` | Global, visible to all agents | `git clone https://github.com/jerryang-cool/trtc-ai-customer-service-skill.git ~/.openclaw/skills/trtc-ai-customer-service` |

Invoke via natural language ("help me build an AI customer service") or slash command `/trtc-ai-customer-service`.

> See [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) for more details.

### CodeBuddy

Settings → Skills → **Import Skill**, then point to this repository's directory. Once imported, mention keywords such as *"AI customer service"*, *"e-commerce support"*, or *"TRTC + AI"* to activate.

### Claude Code

```bash
# User-level (available across all projects)
git clone <repo-url> ~/.claude/skills/trtc-ai-customer-service

# OR project-level (commit to repo, share with team)
git clone <repo-url> .claude/skills/trtc-ai-customer-service
```

Claude Code auto-discovers skills via `description` matching. Invoke implicitly ("help me build an AI customer service") or explicitly via `/trtc-ai-customer-service`.

### OpenAI Codex CLI

```bash
# User-level
git clone <repo-url> ~/.codex/skills/trtc-ai-customer-service

# OR project-level
git clone <repo-url> .agents/skills/trtc-ai-customer-service
```

Codex auto-detects new skills on next session. Invoke implicitly via natural language, or explicitly via `$trtc-ai-customer-service`.

### Cursor

```bash
# Skill bundle: drop into Cursor's skills directory
git clone <repo-url> ~/.cursor/skills/trtc-ai-customer-service
```

The `.cursor/rules/trtc-ai-customer-service.mdc` inside this repo follows the 2026 MDC format (Agent Requested mode) — Cursor's Agent loads it on demand based on the description.

> **Legacy `.cursorrules` users**: Cursor silently ignores `.cursorrules` in Agent mode since 2026. This skill ships only the modern `.cursor/rules/*.mdc` format.

## Quick Start

```bash
# 1. Generate a new project
python scripts/scaffold.py ./my-shop --name "CloudShop" --name-en "CloudShop Mall"

# 2. Launch (first run enters interactive credential wizard)
cd ./my-shop && ./start.sh

# 3. Open http://localhost:8080
```

## Architecture

```
┌─────────────────────────────────┐
│  Browser  (TRTC Web SDK v5)     │
│  WebRTC audio + custom messages │
└──────────────┬──────────────────┘
               │
       ┌───────▼───────┐
       │   TRTC Room   │
       │  ASR → LLM →  │  Cloud-hosted AI pipeline
       │      TTS       │  (zero LLM calls on your server)
       └───────┬────────┘
               │ OpenAPI (TC3-HMAC-SHA256)
       ┌───────▼────────┐
       │  Flask Backend  │  UserSig signing
       │   (app.py)      │  + OpenAPI relay only
       └─────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.8+ · Flask · tencentcloud-sdk-python |
| Frontend | Vanilla JS · TRTC Web SDK v5 · CSS custom properties |
| AI Engine | TRTC ConversationAI (cloud ASR → LLM → TTS) |
| Auth | HMAC-SHA256 UserSig (server-side only) |
| Config | YAML via `envyaml` with env-var interpolation |

## Project Layout

```
trtc-ai-customer-service-skill/
├── SKILL.md              # Skill entry — used by CodeBuddy / Claude Code / Codex CLI
├── .cursor/
│   └── rules/
│       └── trtc-ai-customer-service.mdc  # Cursor 2026 MDC format
├── LICENSE               # MIT
├── CHANGELOG.md          # Version history
├── README.md             # English documentation (this file)
├── README_ZH.md          # 中文文档
├── scripts/
│   └── scaffold.py       # One-command project generator
├── references/
│   ├── architecture.md   # System design & backend integration
│   ├── config-guide.md   # Full configuration reference
│   └── frontend-guide.md # TRTC Web SDK integration guide
└── assets/               # Template files shipped by scaffold
```

## References

- [Tencent RTC Console](https://console.trtc.io/)
- [Conversational AI Solution](https://trtc.io/solutions/conversational-ai)
- [LLM Configuration Guide](https://trtc.io/document/68338?product=conversationalai)
- [TTS Voice Configuration](https://trtc.io/document/79682?product=conversationalai)

## License

Released under the [MIT License](LICENSE).
