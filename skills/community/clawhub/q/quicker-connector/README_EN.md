# Quicker Connector - OpenClaw Skill

[English](README_EN.md) | [中文](README.md)

A powerful OpenClaw skill for integrating with Quicker automation tool. Read, search, and execute Quicker actions with AI-powered natural language matching.

[中文文档](README.md) | [GitHub Releases](https://github.com/awamwang/quicker-connector/releases)

---

## ✨ Features

- 📊 **Dual Data Sources** - Support both CSV and SQLite database
- 🔍 **Multi-field Search** - Search by name, description, type, panel
- 🧠 **AI Matching** - Natural language understanding with keyword extraction
- 🎯 **Precise Execution** - Sync/async action execution with parameter support
- 📈 **Statistics** - Complete action categorization and panel distribution
- 🔧 **Encoding Adaptive** - Auto-detect UTF-8/GBK and other encodings
- 📤 **JSON Export** - One-click export of complete action list

---

## 🚀 Quick Start

### Installation

#### Method 1: GitHub Release (Recommended)

```bash
# Download latest version
wget https://github.com/awamwang/quicker-connector/releases/download/v1.2.0/quicker-connector-1.2.0.tar.gz

# Extract
tar -xzf quicker-connector-1.2.0.tar.gz

# Copy to OpenClaw skills directory
cp -r quicker-connector/* ~/.openclaw/workspace/skills/quicker-connector/

# Restart OpenClaw Gateway
openclaw gateway restart
```

#### Method 2: ClawHub

```bash
clawhub install quicker-connector
```

#### Method 3: Git Clone (Developers)

```bash
git clone https://github.com/awamwang/quicker-connector.git ~/.openclaw/workspace/skills/quicker-connector
openclaw gateway restart
```

---

## 📊 Data Structure

### QuickerAction

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique identifier |
| `name` | str | Action name |
| `description` | str | Action description |
| `action_type` | str | Action type (XAction/SendKeys/RunProgram) |
| `uri` | str | Execution URI (quicker:runaction:xxx) |
| `panel` | str | Panel/category |
| `exe` | str | Associated program name |
| `create_time` | str | Creation time |
| `update_time` | str | Update time |

### QuickerActionResult

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Success status |
| `output` | str | Standard output |
| `error` | Optional[str] | Error message |
| `exit_code` | Optional[int] | Exit code |

---

## ⚙️ Configuration

Config file: `~/.openclaw/workspace/skills/quicker-connector/config.json`

```json
{
  "csv_path": "/root/.openclaw/workspace/data/QuickerActions.csv",
  "db_path": "C:\\Users\\Administrator\\AppData\\Local\\Quicker\\data\\quicker.db",
  "starter_path": "C:\\Program Files\\Quicker\\QuickerStarter.exe",
  "default_source": "csv",
  "auto_select_threshold": 0.8,
  "max_results": 10
}
```

### Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `csv_path` | string | "" | Quicker actions CSV path |
| `db_path` | string | "" | Quicker database path |
| `starter_path` | string | "C:\\Program Files\\Quicker\\QuickerStarter.exe" | QuickerStarter.exe path |
| `default_source` | string | "csv" | Default data source |
| `auto_select_threshold` | float | 0.8 | Auto-execution threshold |
| `max_results` | int | 10 | Maximum results |

---

## 🔧 Advanced Features

### JSON Export

```python
connector.export_to_json("actions.json")
```

### Statistics

```python
stats = connector.get_statistics()
print(f"Total: {stats['total']}")
print("Types:", stats['by_type'])
print("Panels:", stats['by_panel'])
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🔗 Links

- [OpenClaw Docs](https://docs.openclaw.ai)
- [Quicker Website](https://getquicker.net/)
- [ClawHub](https://clawhub.ai)
- [GitHub Repo](https://github.com/awamwang/quicker-connector)
- [中文文档](README.md)

---

## 📝 Changelog

### v1.2.0 (2026-03-28)
- ✅ Advanced Skill Creator optimization
- ✅ Full OpenClaw compliance
- ✅ Natural language triggers
- ✅ System prompt and thinking model
- ✅ Enhanced settings
- ✅ GitHub release ready
- ✅ Complete Chinese documentation

---

**Note**: This skill requires Windows and Quicker software to function properly.
