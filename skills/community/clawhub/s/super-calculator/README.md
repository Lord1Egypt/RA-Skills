# 全能超级计算器 | All-Powerful Calculator

> 🧮 一句话触发，什么都能算 | Trigger with one sentence, calculate anything

---

## 简介 | Introduction

**全能超级计算器**是一款 OpenClaw 智能体技能，让 AI 能够处理日常生活中几乎所有的计算需求——从简单的加减乘除，到复杂的复利贷款、健康指标，只需一句话，AI 即可给出完整计算过程与精确结果。

**All-Powerful Calculator** is an OpenClaw agent skill that enables AI to handle virtually any calculation need in daily life — from simple arithmetic to complex compound interest, loan repayments, and health metrics. Just speak your request in natural language and get complete calculation steps with precise results.

---

## 功能亮点 | Key Features

| 功能 | 说明 | Feature | Description |
|------|------|---------|-------------|
| 💰 金融计算 | 复利、单利、贷款月供、理财收益 | 💰 Finance | Compound/Simple interest, loan EMI, investment returns |
| 📅 日期计算 | 年龄、日期间隔、工作日 | 📅 Date & Time | Age, date diff, business days |
| 🔢 统计分析 | 均值、方差、标准差、中位数 | 🔢 Statistics | Mean, variance, std dev, median |
| 📐 单位换算 | 长度、重量、温度、面积 | 📐 Unit Conversion | Length, weight, temp, area |
| 🏃 健康指标 | BMI、BMR、每日所需热量 | 🏃 Health | BMI, BMR, daily calories |
| 📊 方程求解 | 一元一次、一元二次方程 | 📊 Equations | Linear, quadratic equations |
| 🧮 基础算术 | 幂、开方、对数、三角函数 | 🧮 Basic Math | Powers, roots, logs, trigonometry |

---

## 快速开始 | Quick Start

### 触发方式 | How to Trigger

直接用自然语言描述你的计算需求即可，AI 会自动识别并调用技能：

Just describe your calculation in natural language:

```
"帮我计算 100 万贷款 20 年要还多少利息"
"Calculate compound interest: principal 100k, rate 5%, 20 years"

"1988年7月1日出生，现在几岁？"
"I was born July 1, 1988, how old am I?"

"175cm，70kg，帮我算BMI"
"I'm 175cm and 70kg, calculate my BMI"

"华氏80度等于摄氏多少度？"
"Convert 80°F to Celsius"
```

### 示例计算 | Example Calculations

**贷款月供计算：**
```
输入：贷款 200 万，年利率 4.9%，20 年还清
月供 = P×[r(1+r)^n] / [(1+r)^n - 1]
月供 ≈ 13,044 元
总利息 ≈ 1,130,560 元
```

**复利计算：**
```
输入：本金 10 万，年复利 5%，存 20 年
公式：F = P × (1 + r)^n
终值 ≈ 265,330 元（本金的 2.65 倍）
```

---

## 目录结构 | Directory Structure

```
全能超级计算器/
├── SKILL.md              # 技能核心文件 | Core skill file
├── scripts/
│   └── calculator.py     # 计算函数库 | Calculation library
├── references/
│   └── formulas.md       # 公式参考手册 | Formula reference guide
└── assets/               # 资源目录（预留）| Reserved for assets
```

---

## 使用限制 | Usage Notes

- 本技能由 AI 驱动，**无需 API Key**，完全本地运行
- 计算精度适合日常生活与参考用途，高精度金融场景请另行验证
- 汇率数据为参考值，实时汇率请以官方数据为准

- This skill is AI-powered and **requires no API Key** — runs entirely locally
- Calculation precision is suitable for daily life and reference purposes
- Exchange rates are reference values; verify with official sources for precision needs

---

## 安装 | Installation

将 `全能超级计算器` 文件夹放入 `~/.qclaw/skills/` 即可：

Place the `全能超级计算器` folder into `~/.qclaw/skills/`:

```bash
cp -r 全能超级计算器 ~/.qclaw/skills/
```

---

## 技术栈 | Tech Stack

- **语言：** Python 3
- **依赖：** 仅标准库（math, datetime, collections）
- **兼容性：** macOS / Linux / Windows

---

## 开源协议 | License

MIT License

---

*🧮 让计算无处不在 | Calculating everywhere, always*
