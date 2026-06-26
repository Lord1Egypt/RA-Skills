# Yunshi — All-in-One Chinese Astrology Skill

> BaZi · ZiWei DouShu · QiMen DunJia · I Ching · Feng Shui · Marriage Compatibility — with daily fortune push. No API required.

[![clawhub](https://img.shields.io/badge/clawhub-yunshi-blue)](https://clawhub.ai/skills/yunshi)
[![version](https://img.shields.io/badge/version-1.2.6-green)](https://clawhub.ai/skills/yunshi)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

## What it does

Yunshi is the most comprehensive Chinese astrology skill on clawhub — covering all major traditional divination systems in one install. Built-in algorithms for BaZi and ZiWei DouShu calculations; no external API or subscription needed.

**BaZi (八字)** — Four Pillars birth chart, year/month/day/hour pillars, Da Yun major cycles  
**ZiWei DouShu (紫微斗数)** — Purple Star Astrology full chart with palace interpretations  
**QiMen DunJia (奇门遁甲)** — strategic divination for decision-making  
**I Ching (易经)** — 64 hexagram readings with changing lines  
**Feng Shui (风水)** — home/office layout analysis and recommendations  
**Marriage compatibility (合婚)** — BaZi compatibility analysis for couples  
**Daily fortune push** — daily luck ratings across career, wealth, love, health

## Installation

```bash
openclaw install yunshi
```

## Usage

```bash
# Daily fortune
openclaw run yunshi daily --birth "1990-05-15 08:30" --gender male

# BaZi full chart
openclaw run yunshi bazi --birth "1990-05-15 08:30"

# ZiWei DouShu
openclaw run yunshi ziwei --birth "1990-05-15 08:30" --gender male

# Marriage compatibility
openclaw run yunshi marriage --birth1 "1990-05-15" --birth2 "1992-08-22"

# I Ching divination
openclaw run yunshi meihua

# Feng shui advice
openclaw run yunshi fengshui
```

## Data & Privacy

- **Local-only profiles.** User data lives in `data/profiles/<userId>.json` on your machine and is never uploaded by the skill itself.
- **Ships with template only.** The published package contains only `data/profiles/template.json`. Real profiles are excluded via `.clawhubignore` and `.gitignore`.
- **Recommended permissions.** `chmod 700 data/profiles && chmod 600 data/profiles/*.json`.
- **Deletion.** Remove the corresponding `data/profiles/<userId>.json` to stop daily push and discard the record — no hidden caches.
- **Do not commit populated profiles** to public repos or paste them into chat.

## Trigger phrases

- **English:** "my horoscope", "daily horoscope", "horoscope now", "cast I Ching", "throw a hexagram", "BaZi chart", "Four Pillars reading", "ZiWei reading", "marriage compatibility", "feng shui layout", "lucky color today"
- **中文:** 算命、今日运势、八字排盘、紫微斗数、占卜、起卦、合婚、看风水、流年大运
- **多语言:** 운세 (KR), 運勢 (JA), tử vi (VN)

## Keywords

Chinese astrology · fortune telling · daily horoscope · divination · BaZi · Four Pillars · ZiWei DouShu · Purple Star Astrology · I Ching · feng shui · marriage compatibility · QiMen DunJia · horoscope push · 算命 · 八字 · 今日运势 · 紫微斗数 · 占卜 · 合婚 · 风水 · 命理 · 流年 · 운세 · 運勢 · tử vi

## Looking for daily luck readings?

For lightweight daily fortune (lucky color / direction / number, interview luck, couple compatibility, weekly / monthly horoscope), try **[lucky-today](https://clawhub.ai/skills/lucky-today)** — yunshi's prompt-only sister skill, no Node deps, bilingual CN/EN.

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/yunshi)
