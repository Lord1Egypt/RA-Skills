# 题材库分析师 / A-Share Theme Analyst

> **subject-library** — AI Agent skill for analyzing China A-share market themes (题材) based on real-time data from 爱投顾 (iTougu) Theme Library.

---

## 🇨🇳 简介

基于爱投顾「题材库」数据的 AI 题材分析技能。支持：

- 📊 题材库完整列表浏览与热度排名
- 🔍 单题材深度分析（结构树、龙头/中军、驱动逻辑）
- 📈 核心个股实时行情获取与资金分析
- ⚡ 主线/板块联合分析（跨题材聚合、分化研判）
- 🔗 个股-题材关联查询
- 🤖 AI 综合研判与趋势预测

**适用市场**: 中国 A 股  
**语言**: 技能内容为中文，frontmatter 为英文

---

## 🇺🇸 Overview

AI agent skill for comprehensive analysis of China A-share market themes (题材/concepts/sectors). Built on real-time data from the iTougu Theme Library API.

**Capabilities:**
- Full theme list browsing with heat ranking
- Single theme deep analysis (structure tree, leader stocks, drivers)
- Core stock real-time quotes with fund flow analysis
- Multi-theme "main line" analysis (cross-theme aggregation)
- Stock-to-theme correlation lookup
- AI-powered market insights and trend prediction

**Target Market**: China A-shares only  
**Language**: Skill content in Chinese, metadata in English

---

## 📦 Installation

### Via ClawHub

```bash
npx clawhub@latest install subject-library
```

### Manual

Copy the `subject-library/` folder into your agent's skills directory.

---

## 📁 File Structure

| File | Purpose |
|------|---------|
| `skill.md` | Main skill instructions for AI agent (Chinese) |
| `api-reference.md` | API specifications, field mappings, complete Python scripts |
| `analysis-templates.md` | 6 output templates + scoring system + search integration |
| `README.md` | This file (human-readable introduction) |
| `LICENSE` | MIT-0 license |

---

## 🔒 Security & Data Sources

This skill accesses the following **public, free, no-authentication-required** APIs. All URLs are well-known financial data endpoints used by millions of retail investors in China.

### Primary APIs (Theme Data)

| URL | Provider | Purpose | Auth |
|-----|----------|---------|------|
| `https://group-api.itougu.com/teach-hotspot/subject/fullList` | 爱投顾 (iTougu) | Theme list with rankings | None |
| `https://group-api.itougu.com/teach-hotspot/subject/subjectDetail4Free` | 爱投顾 (iTougu) | Theme detail with stock tree | None |

### Supplementary APIs (Stock Quotes)

| URL | Provider | Purpose | Auth |
|-----|----------|---------|------|
| `http://qt.gtimg.cn/q=...` | 腾讯财经 (Tencent Finance) | Real-time stock quotes (preferred) | None |
| `https://push2.eastmoney.com/api/qt/ulist.np/get` | 东方财富 (East Money) | Stock quotes fallback | None |

### Optional Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| [AKShare](https://github.com/akfamily/akshare) | Final fallback for stock data | `pip install akshare` |

**No credentials, API keys, or user tokens are required or collected by this skill.**

All external API calls are read-only GET/POST requests to publicly accessible financial data endpoints. No data is sent to any third-party service beyond the query parameters documented above.

---

## ⚠️ Disclaimer

- This skill is for **informational purposes only** and does not constitute investment advice.
- All analysis outputs include mandatory risk disclaimers.
- AI predictions are clearly labeled as such (⚠️ AI预测，谨慎参考).
- Data accuracy depends on upstream API availability.

---

## 📄 License

[MIT-0](./LICENSE) — Free to use, modify, and redistribute. No attribution required.
