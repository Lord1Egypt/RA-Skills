# Smart Poller

> Periodically polls a Feishu (Lark) task board and auto-executes tasks assigned to the current AI agent.

**Version**: v1.0 | **Author**: socneo | **Category**: automation

📖 [中文文档 README.zh-CN.md](README.zh-CN.md)

---

## ✨ Features

- ✅ **Scheduled polling** — configurable interval (default: 15 min)
- ✅ **Feishu integration** — full Feishu Docs API support
- ✅ **Silent mode** — no notification when no tasks; saves ~95% Token usage
- ✅ **Task parsing** — auto-detects pending tasks assigned to the current agent
- ✅ **Auto feedback** — writes completion feedback back to the Feishu document
- ✅ **Dual runtime** — Node.js and Python versions available

---

## 📦 Installation

```bash
# Option 1: Install via ClawHub (recommended)
clawhub install smart-poller

# Option 2: Copy manually
cp -r smart_poller /your/workspace/
cd /your/workspace/smart_poller
cp config.example.json config.json
```

---

## 🔧 Configuration

Edit `config.json`:

```json
{
  "app_id": "cli_xxxxxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "doc_token": "xxxxxxxxxxxxxxxxxxxxxxxxx",
  "assignee": "your_agent_id",
  "poll_interval_minutes": 15,
  "silent_mode": true
}
```

| Field | Description | Example |
|-------|-------------|---------|
| `app_id` | Feishu App ID | `cli_xxxxxxxxxxxxx` |
| `app_secret` | Feishu App Secret | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `doc_token` | Task board document ID (from URL) | `xxxxxxxxxxxxxxxxxxxxxxxxx` |
| `assignee` | Current agent identifier | `agent1` / `agent2` |
| `poll_interval_minutes` | Polling interval (minutes) | `15` |
| `silent_mode` | Suppress notifications when idle | `true` |

> 🔑 Get `app_id` and `app_secret` from [Feishu Open Platform](https://open.feishu.cn/app).

---

## 🚀 Usage

### Python

```bash
# Run once (for testing)
python3 poller.py config.json --once

# Continuous polling (production)
python3 poller.py config.json
```

### Node.js

```bash
# Run once (for testing)
node poller.js --once

# Continuous polling (production)
node poller.js
```

### Cron (recommended for production)

```bash
# Edit crontab
crontab -e

# Run every 15 minutes
*/15 * * * * cd /path/to/smart_poller && python3 poller.py config.json --once
```

---

## 📊 Task Board Format

Smart Poller recognizes tasks in the following format:

```
[TASK-XXX-001] [Test] Verify task board write
Assign: agent_a → agent_b  |  Priority: medium  |  Status: pending
Due: 2026-03-16  |  Created: 2026-03-16 11:30
Description: Please verify the polling mechanism is working correctly.
```

**Completion feedback format:**
```
[agent_b completed] TASK-XXX-001 | Time: 2026/3/16 12:28:14 | Result: Verification successful
```

---

## 🧩 Real-World Example

**Scenario**: Multi-agent async task execution

Each agent runs its own poller with a unique `assignee`, all sharing the same task board:

```json
// Agent A config
{ "assignee": "agent_a", "poll_interval_minutes": 15 }

// Agent B config
{ "assignee": "agent_b", "poll_interval_minutes": 30 }
```

**Results from field testing** (4-hour continuous run):
- 17+ successful polling rounds
- Success rate: 100%
- Token savings: ~95% (silent mode)

---

## 🏗️ Architecture

```
smart_poller/
├── poller.py              # Python entry point
├── poller.js              # Node.js entry point
├── config.example.json    # Config template
├── README.md              # This file (English)
├── README.zh-CN.md        # Chinese documentation
├── SKILL.md               # OpenClaw skill descriptor
└── requirements.txt       # Python stdlib only, no pip install needed
```

### Core Classes (Python)

| Class | Responsibility |
|-------|---------------|
| `FeishuAPI` | Feishu API wrapper (token management, HTTP requests) |
| `TaskParser` | Parse task board content (regex matching, status detection) |
| `SmartPoller` | Main poller (config loading, polling loop, task execution) |

---

## 📝 Changelog

### v1.0.0 (2026-03-17)
- ✅ Initial release
- ✅ Python / Node.js dual runtime
- ✅ Silent mode optimization
- ✅ Full Feishu Docs API integration

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

- Report bugs
- Suggest new features
- Share use cases

GitHub: https://github.com/openclaw/skills

---

## 📄 License

MIT License

---

## 🙏 Acknowledgements

- Inspired by AI team async collaboration practices (2026-03-16)
- Platform: [Feishu Open Platform](https://open.feishu.cn), [OpenClaw](https://openclaw.ai)

---

*Last updated: 2026-03-18*
