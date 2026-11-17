---
name: Vibe Coding Rules
id: vibe-coding-rules
version: 2.5.2
primary: true
description: >
  6个自我进化的AI编程纪律Skill。改代码前强制自查→安全执行→改后28条规则扫描→自动化测试→变更日志，一条龙闭环。
  🍞独家面包屑系统：文件自动记住耦合关系和历史坑位。信任分级规则自生长：重复Bug升级为硬规则。
  由代码小白用AI写14万行代码的踩坑经验沉淀。支持CodeBuddy/Cursor/Windsurf。Apache 2.0。
  6 self-evolving AI coding discipline Skills. Pre-check → Safe exec → 28-rule post-check → Auto-test → Changelog. Closed loop.
  🍞 Breadcrumb auto-seeding. Trust-tiered rule growth. Built from 140K lines of real-world pain. Apache 2.0.
tags:
  - vibe-coding
  - ai-coding
  - code-quality
  - coding-assistant
  - developer-tools
  - self-check
  - testing
  - pipeline
  - breadcrumb
  - self-growing
category: 开发工具
author: 躺不平联盟
website: https://tangbuping.com
license: Apache-2.0
---

# Vibe Coding Rules V2.5

> **AI 写代码最大的敌人，是它自己——它会忘记昨天修好的 Bug，会在同一个坑里反复跌倒。**
>
> 6 个会自我进化的 Skill，给 AI 装上"编程纪律"。从改前自查到变更记录，一条流水线闭环交付。
>
> **AI's biggest enemy is itself — it forgets the bugs it fixed yesterday.**
> 6 self-evolving Skills. Pre-check → Safe exec → Post-check → Auto-test → Changelog. Closed loop.

---

## ⚡ Before & After / 装前装后

| 场景 | 没装之前 | 装了之后 |
|:--|:--|:--|
| 数值 0 被当 false 吞掉 | 每次排查半小时 | coding-principles 改前就拦住了 |
| `<select>` 假选中 | 用户反馈才修 | safe-terminal-executor 脚本自验证 |
| 同一个 Bug 犯第 3 次 | AI 毫无记忆 | self-check 自动升级为硬规则，永不再犯 |
| 改完代码不知道影响谁 | 发布后炸了才知道 | 🍞面包屑标出耦合文件，改前就提醒 |

---

## 📦 Install / 安装

```bash
# CodeBuddy / Cursor / Windsurf
openclaw skills install @ron-dali/vibe-coding-rules

# 或手动
git clone https://github.com/Ron-dali/vibe-coding-rules.git
```

安装后对 AI 说：**"初始化流水线"**，AI 自动检测项目并配置。

---

## Pipeline Architecture / 流水线架构

```
coding-principles (5 Principles + 🍞 Breadcrumb Pre-scan / 改前五大原则 + 面包屑预扫描)
  → safe-terminal-executor (Safe Terminal Exec / 安全终端执行)
    → Write/Modify Code / 编写修改代码
      → self-check (28 Rules + Breadcrumb Seeding / 28条规则自检 + 面包屑播种)
        → web-testing (Auto Regression Test / 自动化回归测试)
          → changelog (Changelog + Growth Detection / 变更日志 + 生长检测)
            → ✅ Closed Loop / 闭环交付
```

## Included 6 Skills / 包含的 6 个 Skill

| Skill | Function / 功能 |
|-------|------|
| 🥇 `coding-principles` | Pre-code 5-principle self-check + 3 trap auto-intercept / 改代码前强制自检五大原则 + 3个常见陷阱自动拦截 |
| 🛡️ `safe-terminal-executor` | Safe terminal wrapper, timeout protection + forced exit / 终端命令安全封装，超时保护+强制退出 |
| 🔍 `self-check` | Post-code 28-rule scan + trust-tiered growth + 🍞 breadcrumb auto-seeding / 改后28条规则逐项检查+信任分级+🍞面包屑播种 |
| 🧪 `web-testing` | DOM assertion + screenshot + OCR automated regression test / DOM断言+截图+OCR自动化回归测试 |
| 📝 `changelog` | Auto changelog generation + rule growth detection / 变更日志自动生成+规则生长检测 |
| 🚀 `pipeline-init` | One-click project pipeline bootstrap / 新项目一键初始化流水线 |

## Core Features / 核心特性

- 🔄 **Self-Growing Rules / 规则自生长** — Today's pitfall becomes tomorrow's hard rule the AI can't break / 今天踩的坑，明天变成AI不能再犯的硬规则
- 🍞 **Breadcrumb System V2.5 / 面包屑系统** — Auto-plant coupled files + historical gotchas in file headers, AI never forgets / 文件头部自动播种耦合关系+历史坑位，AI不再失忆
- 🎯 **Trust-Tiered Growth / 信任分级** — Tier0 Observation Pool → Tier1 [SOFT] → Tier2 [HARD], auto promote/demote / 观察池→软规则→硬规则，自动晋升退役
- 🌍 **Cross-Platform / 跨界兼容** — Works with CodeBuddy, Cursor, Windsurf / 三种AI Agent通用

## Who Needs This? / 谁需要这个？

- 🐣 AI coder who doesn't know programming → Discipline exoskeleton / 用AI写代码但不懂编程 → 编程纪律外骨骼
- 💻 Solo dev / one-person company → Your own QA team / 独立开发者一人公司 → 自己的QA团队
- 🏢 Small team using AI assistance → Unified quality standards / 小型团队用AI辅助 → 统一质量标准
- 🤖 Heavy AI Agent user → Agent gets smarter over time / 重度AI Agent用户 → Agent越用越聪明

## Author / 作者

躺不平联盟 (TangBuPing) — A coding beginner who wrote 140,000 lines of code across a 3-platform system with AI, distilling every painful lesson into these 6 Skills.
代码小白用AI写140000行三端平台，把踩坑经验沉淀为这6个Skill。

[GitHub](https://github.com/Ron-dali/vibe-coding-rules) · [tangbuping.com](https://tangbuping.com)
