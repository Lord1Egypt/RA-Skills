# 🐙 SkillHub Daily — China-Focused Skill Insights

> Daily scan of SkillHub.cn's 75,000+ skill ecosystem, recommending 8 skills via 7 dimensions, focused on **China adaptation** and **active developers**

中文 | [English](./README.md)

![Version](https://img.shields.io/badge/Version-7.0.1-blue)
![Platform](https://img.shields.io/badge/Platform-SkillHub.cn-green)
![License](https://img.shields.io/badge/License-MIT--0-orange)

---

## What is SkillHub Daily?

SkillHub Daily is a daily recommendation engine that scans SkillHub.cn's 7 ranking lists + 11 category searches + keyword searches (1000+ candidates), selecting 8 skills via a 7-dimension algorithm.

Complementary to [ClawHub Daily](https://clawhub.ai): ClawHub Daily focuses on curated quality and trend insights (500 skills), while SkillHub Daily focuses on **China adaptation**, **active developer discovery**, and **dual-lab security audit** (75,000+ skills).

## Key Features

| Feature | Description |
|---------|-------------|
| 🇨🇳 China First | Prioritize skills adapted for China ecosystem (Feishu/WeChat/DingTalk/Xiaohongshu/Douyin) |
| 👤 Active Developers | Discover prolific developers and their representative works |
| 🔬 Security Audit | Call skillhub skill reports for dual-lab security assessment |
| 📊 AI Quality Eval | Call skillhub skill evaluation for 6-dimension scoring |
| 🧠 3-Level Memory Collision | project_memory×3 / topics×2 / user_profile×1 |
| 🚫 7-Day Dedup | Cross-dimension dedup to avoid repeated recommendations |

## 7-Dimension Recommendation Algorithm

| Dimension | Count | Description |
|-----------|-------|-------------|
| 🔥 Trending Surge | 2 | On both hot + trending lists |
| 🚀 Newcomers | 1 | Released within 30 days + installs > 100 |
| 🎯 Scene Match | 2 | 7 pain-point scene library matching |
| 🧠 Memory Collision | 1 | 3-level weighted keyword collision |
| 🇨🇳 China First | 1 | China adaptation signal detection (25 keywords) |
| 👤 Active Developer | 1 | Representative work from prolific developers |
| 🏢 Official Verified | 1(optional) | verified=true |

## Installation

```bash
# 1. Install skillhub CLI
npm i -g skillhub

# 2. Login
skillhub auth login

# 3. Clone the skill
git clone https://github.com/EdwardWason/skillhub-daily.git
```

## Usage

### Manual Execution

```bash
# One-click (fetch → recommend → push to 3 destinations)
python skillhub_cn_daily_executor.py

# Generate briefing only, no push
python skillhub_cn_daily_executor.py --skip-push

# Skip deep evaluation (save time)
python skillhub_cn_daily_executor.py --skip-eval
```

### Scheduled Task

TRAE Schedule task configured (ID: be17fc27), runs daily at 06:50 Beijing time.

> **User Notice**: Running this skill automatically writes recommendation briefings to Obsidian, IMA knowledge base, and Feishu cloud docs. Briefings include recommendation results based on local project memory keywords (no raw memory content is transmitted). Use `--skip-push` to disable pushing.

## Triple Storage

| Destination | Method | Config |
|-------------|--------|--------|
| Obsidian inbox | Markdown + frontmatter | OBSIDIAN_VAULT_PATH |
| IMA FIM Knowledge Base | Two-step (create_note + add_knowledge) | IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY / IMA_KB_ID |
| Feishu Cloud Doc | lark-cli / lark-doc skill | Feishu auth |

> **Credential Security**: All credentials are passed via environment variables, never hardcoded. Ensure environment variables are configured locally only and never committed to version control.

## Complementary to ClawHub Daily

| | SkillHub Daily | ClawHub Daily |
|---|---|---|
| Platform | SkillHub.cn (75K+) | ClawHub.ai (500) |
| Focus | 🇨🇳 China / 👤 Developers / 🔬 Audit | 🦞 Curated / Trends |
| Evaluation | AI 6-dim + Dual-lab audit | Rating + Activity |
| Collision | 3-level weighted memory | Pain-point keyword match |

## Project Structure

```
skillhub-cn-daily/
├── SKILL.md                          # Skill definition
├── skillhub_cn_daily_executor.py     # One-click executor
├── scripts/
│   ├── fetch_skillhub_cn.py          # Data fetcher
│   └── daily_recommend.py            # Recommendation engine
├── data/                             # Runtime data (gitignored)
├── .claude-plugin/plugin.json        # Plugin config
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Dependencies

- Python 3.8+
- skillhub CLI (`npm i -g skillhub`)
- Authenticated skillhub auth

## License

MIT-0
