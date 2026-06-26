# Smart Poller Skill

**Smart Polling Skill** — Periodically polls a Feishu task board and auto-executes tasks assigned to the current AI agent.

📖 [中文文档](README.zh-CN.md)

---

## 🎯 Features

- ✅ Scheduled polling of Feishu task board (configurable interval)
- ✅ Auto-detect tasks assigned to the current AI agent
- ✅ Silent mode (no notification when idle; saves ~95% Token usage)
- ✅ Auto-write completion feedback to the task board
- ✅ Node.js and Python dual runtime support

---

## 📦 Installation

```bash
clawhub install smart-poller
```

---

## 🔧 Configuration

Copy the config template and fill in your values:

```bash
cp config.example.json config.json
```

**Required fields:**
- `app_id`: Feishu App ID
- `app_secret`: Feishu App Secret
- `doc_token`: Task board document ID
- `assignee`: Current agent identifier

---

## 🚀 Usage

```bash
# Run once (testing)
python3 poller.py config.json --once

# Continuous polling (production)
python3 poller.py config.json

# Cron (recommended)
*/15 * * * * python3 poller.py config.json --once
```

---

## 🛠️ Required Tools

- `exec`: Run Python/Node.js scripts
- `file_read`: Read config file
- `file_write`: Write config and logs

---

## 📝 Changelog

### v1.0.0 (2026-03-17)
- ✅ Initial release
- ✅ Full Feishu API integration
- ✅ Silent mode optimization
- ✅ Dual runtime support

---

## 🤝 Contributing

GitHub: https://github.com/openclaw/skills

---

## 📄 License

MIT License

---

**Author**: socneo  
**Last updated**: 2026-03-18
