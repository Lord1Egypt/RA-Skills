# 🛡️ Safe Self-Improving Agent

> **隐私优先的自我进化技能** — 自动脱敏 · 重复检测 · 智能技能生成

[![ClawHub](https://img.shields.io/badge/ClawHub-safe--self--improving-blue)](https://clawhub.ai/hjfl888/safe-self-improving)
[![Version](https://img.shields.io/badge/version-0.3.0-green)]()
[![Security](https://img.shields.io/badge/security-clean-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT--0-orange)]()

## ❓ Why This Exists

Many self-improving AI agent skills on ClawHub have security concerns:
- Auto-executing hooks that run without user consent
- Cross-session communication that reads other sessions' data
- Silent modification of system files
- No sensitive data masking

**This skill does things differently** — every operation requires your explicit confirmation, and sensitive data is automatically sanitized.

## 🆚 Key Differentiators

| Feature | Typical Self-Improving Skills | 🛡️ Safe Self-Improving |
|---------|-------------------------------|------------------------|
| Auto-executing hooks | Often present | ❌ **None** |
| Cross-session communication | Sometimes present | ❌ **None** |
| Silent file modification | Sometimes present | ❌ **None** (`.learnings/` only) |
| Auto-execute improvements | Often automatic | ❌ **User confirms all** |
| Sensitive data masking | Rarely available | ✅ **Auto-masked** (6 types) |
| Duplicate detection | Rarely available | ✅ **Keyword matching + tracking** |
| 🆕 Smart Skill Synthesis | Not available | ✅ **Auto-generate skills from patterns** |
| 🆕 Learning Export | Not available | ✅ **JSON + Markdown dual format** |
| 🆕 Learning Analytics | Not available | ✅ **Domain heatmap + resolution rate** |

## ✨ Features

### Core
- 📝 **Learning Capture** — Record lessons, errors, and best practices with user confirmation
- 🔍 **Smart Review** — Browse all learnings with statistics and priority analysis
- 📊 **Task Evaluation** — Rate task performance across 5 dimensions
- 🔒 **Auto Masking** — Sensitive data (API keys, tokens, emails, IPs, phone, IDs) automatically sanitized
- 🔁 **Duplicate Detection** — Won't record the same lesson twice; tracks occurrence count
- 📁 **Sandboxed Storage** — All data in `.learnings/` directory only, never touches system files

### 🆕 New in v0.3.0
- 🧬 **Smart Skill Synthesis** — Automatically discovers recurring patterns in your learnings and generates new skill drafts (SKILL.md) you can install or publish
- 📤 **Learning Export** — Export all records in JSON (structured) or Markdown (readable) format
- 📈 **Learning Analytics** — Visual domain heatmap, resolution rate, frequency trends, and skill generation readiness indicators

## 📦 Install

```bash
openclaw skills install safe-self-improving
```

## 🚀 Usage

Just start chatting with your agent. When you notice something worth remembering:

| Say This | What Happens |
|----------|-------------|
| "记录这个教训" | Log a learning (shows content first, you confirm) |
| "记下这个错误" | Log an error with root cause analysis |
| "这是个好方法" | Record a best practice |
| "回顾学习记录" | Review all learnings with stats |
| "怎么改进" | Get improvement suggestions (won't auto-execute!) |
| "打个分" | Evaluate current task performance |
| 🆕 "生成技能" | Auto-generate a new skill from recurring patterns |
| 🆕 "导出学习记录" | Export all records as JSON + Markdown |
| 🆕 "学习统计" | Show learning analytics and trends |
| "清除学习记录" | Clear all records (requires double confirmation) |

## 📁 Data Storage

All data is stored locally in your project's `.learnings/` directory:

```
your-project/
└── .learnings/
    ├── LEARNINGS.md         # Lessons & best practices
    ├── ERRORS.md            # Error records
    ├── IMPROVEMENTS.md      # Improvement suggestions
    ├── skill-drafts/        # 🆕 Auto-generated skill drafts
    │   └── draft-YYYYMMDD-NNN.md
    ├── export-YYYYMMDD.md   # 🆕 Markdown export
    └── export-YYYYMMDD.json # 🆕 JSON export
```

## 🔒 Security Guarantees

1. ❌ Never records passwords, tokens, API keys, or environment variable values
2. ❌ Never modifies system files or other skills' files
3. ❌ Never accesses other sessions or agents' data
4. ❌ Never registers any hooks
5. ❌ Never auto-executes improvements
6. ✅ Only writes to `.learnings/` directory
7. ✅ All operations require explicit user confirmation
8. ✅ Auto-masks sensitive information before writing

## 📄 License

MIT-0 — Free to use, modify, and distribute.

## 🤝 Contributing

Issues and PRs welcome at [GitHub](https://github.com/hjfl888/safe-self-improving)

---

**Need help installing or configuring?** Feel free to open an issue or reach out!
