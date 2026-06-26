# 💡 Smart Follow-ups

### 🦎 A OpenClaw Skill

> Generate contextual follow-up suggestions for your AI conversations

<p align="center">
  <a href="https://openclaw.com"><img src="https://img.shields.io/badge/🦎_OpenClaw-Skill-7c3aed?style=for-the-badge" alt="OpenClaw Skill"></a>
  <a href="https://clawhub.ai/skills/smart-followups"><img src="https://img.shields.io/badge/ClawHub-Install-22c55e?style=for-the-badge" alt="ClawHub"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.1.4-orange?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/channels-9-blue?style=flat-square" alt="Channels">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License">
</p>

---

**This is a skill for [OpenClaw](https://openclaw.com)** — the AI assistant that works across Telegram, Discord, Signal, WhatsApp, and more.

After every AI response, get **3 smart suggestions** for what to ask next:

- ⚡ **Quick** — Clarifications and immediate questions
- 🧠 **Deep Dive** — Technical depth and detailed exploration
- 🔗 **Related** — Connected topics and broader context

**Telegram/Discord/Slack:** Clickable inline buttons  
**Signal/iMessage/SMS:** Numbered text list

---

## ✨ Features

- **🎯 Context-Aware** — Analyzes your last 1-3 exchanges
- **🔘 Interactive Buttons** — One tap to ask (Telegram, Discord, Slack)
- **📝 Text Fallback** — Numbered lists for channels without buttons
- **⚡ Fast** — ~2 second generation time
- **🔐 Privacy-First** — Uses your existing OpenClaw auth by default
- **🔧 Flexible** — Multiple provider options (see below)

---

## 🦎 What is OpenClaw?

[OpenClaw](https://openclaw.com) is a powerful AI assistant that connects Claude to your favorite messaging apps — Telegram, Discord, Signal, WhatsApp, iMessage, and more. Skills extend OpenClaw with new capabilities.

**Not using OpenClaw yet?** Check out [openclaw.com](https://openclaw.com) to get started!

---

## 🚀 Quick Start

### Installation

```bash
# Via ClawHub (recommended)
clawhub install smart-followups

# Or manually
cd /path/to/openclaw/skills
git clone https://github.com/robbyczgw-cla/smart-followups
cd smart-followups
npm install
```

### Usage

Just say **"followups"** (or "give me follow-ups", "suggestions") in any OpenClaw conversation:

```
You: What is Docker?
Bot: Docker is a containerization platform that...

You: followups

Bot: 💡 What would you like to explore next?
[⚡ How do I install Docker?]
[🧠 Explain container architecture]
[🔗 Docker vs Kubernetes?]
```

Click any button → sends that question automatically!

> **Note:** This works as a keyword the agent recognizes, not as a registered `/slash` command. OpenClaw skills are guidance docs — the agent reads the SKILL.md and knows how to respond when you ask for follow-ups.

---

## 🔐 Authentication

### OpenClaw Native (Default) ⭐

**No API keys needed!** The skill uses your existing OpenClaw authentication — same model and login as your current chat.

- ✅ No additional API keys required
- ✅ Uses your current session's model (Haiku/Sonnet/Opus)
- ✅ Works out of the box

> **Note (v2.1.4):** The handler uses OpenClaw-native auth. External providers (OpenRouter/Anthropic) are only supported via the standalone CLI tool for testing purposes.

---

## ⚙ Configuration

The skill works out of the box with OpenClaw's native authentication. No configuration required!

**Optional:** Add to your `openclaw.json` if you want to customize:

```json
{
  "skills": {
    "smart-followups": {
      "enabled": true,
      "autoTrigger": false
    }
  }
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `enabled` | `true` | Enable/disable the skill |
| `autoTrigger` | `false` | Auto-show follow-ups after every response |

---

## 📱 Channel Support

Works on **every OpenClaw channel** with adaptive formatting:

| Channel | Mode | Interaction |
|---------|------|-------------|
| **Telegram** | Inline buttons | Tap to ask |
| **Discord** | Inline buttons | Click to ask |
| **Slack** | Inline buttons | Click to ask |
| **Signal** | Text list | Reply 1, 2, or 3 |
| **WhatsApp** | Text list | Reply 1, 2, or 3 |
| **iMessage** | Text list | Reply 1, 2, or 3 |
| **SMS** | Text list | Reply 1, 2, or 3 |
| **Matrix** | Text list | Reply 1, 2, or 3 |
| **Email** | Text list | Reply with number |

📖 See [CHANNELS.md](CHANNELS.md) for detailed channel-specific documentation.

---

## 🛠 CLI Tool (Standalone, Optional)

A standalone CLI is included for testing and scripting **outside of OpenClaw**:

```bash
# CLI requires explicit API key and model (not connected to OpenClaw)
export OPENROUTER_API_KEY="sk-or-..."

# Generate follow-ups from JSON context
echo '[{"user":"What is Docker?","assistant":"Docker is..."}]' | \
  node cli/followups-cli.js --model anthropic/claude-3-haiku --mode text

# Output modes: json, telegram, text, compact
node cli/followups-cli.js --model anthropic/claude-3-haiku --mode telegram < context.json
```

> **Note:** The CLI is a standalone tool separate from the core skill. It requires an explicit `--model` flag and API key. The main skill uses OpenClaw-native auth.

See `node cli/followups-cli.js --help` for all options.

---

## 📖 Examples

### Telegram Buttons

```
💡 What would you like to explore next?

[⚡ How do I install Docker?        ]
[🧠 Explain Docker's architecture   ]
[🔗 Compare Docker to Kubernetes    ]
```

### Signal Text Mode

```
💡 Smart Follow-up Suggestions

⚡ Quick
1. How do I install Docker?

🧠 Deep Dive
2. Explain Docker's architecture

🔗 Related
3. Compare Docker to Kubernetes

Reply with 1, 2, or 3 to ask that question.
```

---

## ❓ FAQ

### Why 3 suggestions instead of 6?

Cleaner UX, especially on mobile. Each category (Quick, Deep, Related) gets one focused suggestion instead of overwhelming you with options.

### Can I use this without OpenClaw?

Yes! The CLI tool works standalone with OpenRouter or Anthropic API keys. But the best experience is integrated with OpenClaw.

### How does it know what to suggest?

The skill analyzes your last 1-3 message exchanges and generates contextually relevant questions across three categories: quick clarifications, deep technical dives, and related topics.

### Will it work with my custom model?

Yes! With `provider: "openclaw"` (default), it uses whatever model your current chat is using. With other providers, specify the model in config.

### Is my conversation data sent anywhere?

**With OpenClaw native:** Same privacy as your normal chat — processed by your configured AI provider.

**With OpenRouter/Anthropic:** Your recent exchanges are sent to generate suggestions. See their respective privacy policies.

### How much does it cost?

- **OpenClaw native:** Uses your existing chat's API usage
- **OpenRouter/Anthropic:** ~$0.001-0.01 per generation depending on model

---

## 🏗 Project Structure

```
smart-followups/
├── cli/
│   └── followups-cli.js    # Standalone CLI tool
├── handler.js              # OpenClaw command handler
├── package.json
├── README.md               # This file
├── SKILL.md                # OpenClaw skill manifest
├── FAQ.md                  # Frequently asked questions
├── INTERNAL.md             # Development notes
├── CHANGELOG.md            # Version history
└── LICENSE                 # MIT License
```

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test across multiple channels
5. Submit a pull request

---

## 📄 License

MIT © [Robby](https://github.com/robbyczgw-cla)

---

## 🙏 Credits

- Inspired by [Chameleon AI Chat](https://github.com/robbyczgw-cla/Chameleon-AI-Chat)'s smart follow-up feature
- Built for the [OpenClaw](https://openclaw.com) ecosystem
- Powered by Claude

---

**Made with 🦎 by the OpenClaw community**
