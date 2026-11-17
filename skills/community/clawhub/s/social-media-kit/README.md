# 📱 Social Media Kit

> Generate a **complete week of social media content** for all major platforms from a single topic or brand.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Stdlib Only](https://img.shields.io/badge/dependencies-stdlib_only-green.svg)](#)

---

## ✨ What It Does

Give it a topic, brand, or description — get back **21 platform-optimized posts** (7 days × 3 platforms), a **beautiful HTML content calendar**, hashtag suggestions, posting-time recommendations, and **JSON export** for scheduling tools.

```
Input:  "sustainable fashion brand called EcoThreads"
Output: 21 posts + visual calendar + JSON export
```

## 🚀 Quick Start

```bash
# Generate a full week of content
python scripts/social_kit.py generate --topic 'sustainable fashion' --brand 'EcoThreads'

# 14 days, two platforms
python scripts/social_kit.py generate --topic 'AI productivity' --days 14 --platforms twitter,linkedin

# Build HTML calendar from JSON
python scripts/social_kit.py calendar content.json --output calendar.html

# Auto-detect from any text
echo 'organic coffee roastery in Brooklyn' | python scripts/social_kit.py --auto
```

Open `output/calendar.html` in any browser to see your content calendar.

## 📊 Output

| File | Description |
|------|-------------|
| `content.json` | All posts structured for scheduling tools (Buffer, Hootsuite, Later) |
| `calendar.html` | Visual weekly grid — color-coded, print-friendly, shareable |

### HTML Calendar Features
- **Weekly grid**: 7 columns (days) × 3 rows (platforms)
- **Color-coded cards**: 🔵 Educational · 🟢 Promotional · 🟠 Engaging · 🟣 Behind-the-Scenes · 🔵 User-Generated
- **Platform icons** and best posting times
- **Print-friendly** CSS
- **Responsive** design

## 🎯 Content Strategy

Uses the **70-20-10 rule**:

| Type | Ratio | Purpose |
|------|-------|---------|
| 🟦 Educational | 70% | Teach, add value, build authority |
| 🟩 Promotional | 20% | Drive action, conversions |
| 🟧 Engaging | 10% | Spark conversation, community |

Plus **Behind-the-Scenes** and **User-Generated Content** for authenticity.

## 📱 Platform Optimization

| Platform | Char Limit | Hashtags | Style |
|----------|-----------|----------|-------|
| Twitter/X | 280 | 1-2 | Punchy, trending |
| Instagram | 2,200 | 10-15 | Visual, emotional |
| LinkedIn | 3,000 | 3-5 | Professional, insightful |

See [`references/platform-guide.md`](references/platform-guide.md) for full details.

## 🔧 Requirements

- **Python 3.8+**
- **No external dependencies** — pure standard library

## 📁 Project Structure

```
social-media-kit/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── social_kit.py        # Main generator script
└── references/
    ├── content-strategy.md   # 70-20-10 rule, content pillars
    └── platform-guide.md     # Per-platform best practices
```

## 💡 Use Cases

- **Solo founders** — plan a week of content in 5 minutes
- **Agencies** — generate client content calendars at scale
- **Content creators** — never run out of post ideas
- **Startups** — maintain consistent presence across platforms
- **Marketers** — export JSON directly to scheduling tools

## 📄 License

MIT © Denis Voronin
