# ⚽ Soccer Predict — Football Betting Prediction Skill

AI-powered football match prediction & betting analysis system for [OpenClaw](https://github.com/openclaw/openclaw).

[![ClawHub](https://img.shields.io/badge/ClawHub-soccer--predict-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)](CHANGELOG.md)

## Features

- **Automated Data Collection** — Scrapes pre-match data from titan007.com: Asian handicap, over/under, European odds, team fundamentals, lineups, corner kicks, half-time goals
- **5-Step Quantitative Analysis**
  1. Data organization & validation
  2. Fundamental analysis (handicap rationality, line movement, bookmaker intent)
  3. True implied probability calculation (margin-adjusted)
  4. Logistic regression models (Asian handicap + over/under)
  5. EV calculation & betting recommendations
- **Dual Output Modes** — Concise (quick results) or Visual (full HTML reports with charts)
- **Post-Match Review & Learning** — Automated deviation analysis, weight optimization, accuracy tracking
- **Enhanced Over/Under Model** — Half-time goal patterns, corner data, league factors, environmental variables

## Install

```bash
# From ClawHub (recommended)
npx clawhub install soccer-predict

# Or from GitHub
git clone https://github.com/superluigi0309/soccer-predict.git ~/.openclaw/skills/soccer-predict
```

## Quick Start

### Option 1: Match ID

Get the match ID from [titan007.com](https://zq.titan007.com/) → click "数据分析" → the number in the URL:

```
预测比赛 2908467
```

### Option 2: Match Description

```
预测 2026.3.15 09:30 MLS Real Salt Lake vs Austin FC
```

### Post-Match Review

After the match, provide the result for automated learning:

```
复盘 比分 2-1
```

## Output Modes

| Mode | Description |
|------|-------------|
| **Concise** | Best pick, probability, EV, predicted score |
| **Visual** | Full HTML report with data tables, probability bars, formulas |

Default: Visual mode.

## How It Works

```
Match ID/Description
       ↓
┌──────────────┐
│ Data Scraping │ ← titan007.com (odds, lineups, fundamentals)
└──────┬───────┘
       ↓
┌──────────────────────┐
│ 5-Step Analysis      │
│ 1. Data Organization │
│ 2. Fundamentals      │
│ 3. Probability Calc  │
│ 4. Regression Models │
│ 5. EV & Recommend    │
└──────┬───────────────┘
       ↓
   Prediction Output
       ↓
┌──────────────┐
│ Post-Match   │ → Weight auto-optimization
│ Review       │ → Accuracy tracking (target: 70%+)
└──────────────┘
```

## Repository Structure

```
soccer-predict/
├── SKILL.md                     # Skill definition (main entry)
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT
├── clawhub.json                 # ClawHub metadata
└── references/
    ├── data-collection.md       # Data scraping guide
    ├── prediction-framework.md  # Analysis framework
    └── review-framework.md      # Post-match review & learning
```

## Target Accuracy

70%+ for both Asian handicap and over/under predictions through iterative learning.

## License

[MIT](LICENSE) © 2026 superluigi0309

---

## 中文说明

专为 OpenClaw 打造的足球比赛博彩预测与分析系统。

### 安装

```bash
npx clawhub install soccer-predict
```

### 快速使用

提供比赛 ID 或描述即可开始预测：

```
预测比赛 2908467
预测 2026.3.15 09:30 美职业 皇家盐湖城 vs 奥斯汀
```

赛果复盘（自动优化权重）：

```
复盘 比分 2-1
```

### 核心能力

- 自动从 titan007.com 抓取亚盘、大小球、欧赔、基本面、阵容等数据
- 五步量化分析：数据整理 → 基本面 → 概率计算 → 回归模型 → EV 推荐
- 赛后自动复盘，迭代优化权重
- 目标：亚盘 + 大小球双维度 70%+ 准确率
