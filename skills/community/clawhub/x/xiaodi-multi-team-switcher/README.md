# 🔄 xiaodi Multi-Team Switcher System

**4 functional teams + 1 smart switcher, 26 professional Agent roles.**

## 🎯 Teams

| Team | Icon | Members | Function |
|------|------|---------|----------|
| Financial | 📊 | 7 | Stock analysis, investment decisions |
| E-commerce | 🛒 | 8 | Product selection, operations, pricing |
| Media | 🎬 | 7 | Video/image/audio processing |
| Office | 📋 | 4 | Calendar, email, documents |
| Switcher | 🔄 | 1 | Smart team routing |

## 🚀 Quick Start

### Natural Language

```
"分析茅台的投资价值"  → Financial Team
"帮我选一款跨境电商产品" → E-commerce Team
"压缩这个视频" → Media Team
"整理今天的日程" → Office Team
```

The Switcher automatically routes to the right team.

## 📊 Architecture

```
┌─────────────────────────────────┐
│     Smart Switcher (Router)     │
│   Intent → Team Assignment      │
└──────────────┬──────────────────┘
               │
   ┌───────────┼───────────┬───────────┐
   ▼           ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│📊 Fin  │ │🛒 Ecom │ │🎬 Media│ │📋 Office│
│ 7 roles│ │ 8 roles│ │ 7 roles│ │ 4 roles│
└────────┘ └────────┘ └────────┘ └────────┘
```

## 📋 Requirements

| Type | Items |
|------|-------|
| Tools | web_search, exec, browser |
| Binaries | ffmpeg, ImageMagick |
| Optional | whisper, KLING API, Runway API |

## ⚠️ Disclaimer

For reference only. Not financial/business advice.

---

**Version**: 1.0.1  
**Author**: xiaodi  
**Homepage**: https://clawhub.ai/skills/xiaodi-multi-team-switcher