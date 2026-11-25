# 🎯 Trigger Test

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**[English](README.md)** | **中文**

测试你的技能是否真的会触发。Trigger Test 把模拟（或你的真实）用户消息喂给宿主模型读取的同一份 description，逐个评分 hit / miss / false-alarm——专治官方评测工具测不出的静默失灵。

**4 个问题。1 份报告。0 次 API 调用。**

**解决的痛点**：官方 skill-creator 的评测脚本对所有查询都报 0% 触发率（10+ 人独立复现）——而且就算它能跑，也只测"触发了没"，从不测"该安静时安静了吗"。Trigger Test 两个方向都覆盖，用一套可复现、零依赖的协议。

## 目录

<details>
<summary>点击展开</summary>

- [工作原理](#工作原理)
- [两种失败模式](#两种失败模式)
- [测试消息来源](#测试消息来源)
- [安装](#安装)
- [快速开始](#快速开始)
- [文件结构](#文件结构)
- [许可](#许可)

</details>

## 工作原理

```
你所有技能的 description
        │
        ▼
┌──────────────────────────┐
│  每条测试消息 × 每个技能：│
│   Q1 意图匹配吗？         │
│   Q2 关键词证据？         │
│   Q3 有竞争者吗？         │
│   Q4 裁决                │
└────────────┬─────────────┘
             ▼
  🎯 hit / miss / false-alarm
     单技能分 + 全局分
```

不调模型、不连外部 API——Agent 按固定的 4 问协议（references/analysis-protocol.md）得出可复现的裁决。因为线上触发取决于宿主读的东西：就是那份 `description`。

## 两种失败模式

| 失败 | 表现 | 伤害 | 修法 |
|---|---|---|---|
| **Miss**（静默失灵） | 用户打出了确切意图，技能没反应 | 用户以为技能坏了，卸载 | 把漏掉的措辞原样加进 description |
| **False alarm**（误触发） | 邻近意图也把它唤醒 | 打断用户，消耗信任 | 加显式"Do NOT use for…"收窄 |

多数工具只测第一种。Trigger Test 把两种当一等公民，外加 **contested**（两个技能争同一条消息）和 **borderline**（浮现隐藏歧义的边缘判定）。

## 测试消息来源

**A. 自动生成**——从每个技能自己的 description 推导：3 条正向（含最难的那种：同意图、完全不同的措辞）、3 条邻近意图的负向（共享关键词、意图不同）、1 条歧义。零配置。

**B. 你的真实消息**——贴 5-10 条你真实发过、当时希望某技能触发（或别触发）的消息。最高信号。

## 安装

```bash
# ClawHub
clawhub install trigger-test

# 或从源码
git clone https://github.com/Thomaszhou22/skill-trigger-test.git
cp -r skill-trigger-test ~/.openclaw/skills/
```

## 快速开始

对 Agent 说：**"对我所有的技能跑一次触发测试"**——它生成测试集、执行协议、交给你记分卡。带真实消息：**"用这几条消息测试我的技能：……"**

## 文件结构

```
trigger-test/
├── SKILL.md                        # 测试执行器（协议 + 评分 + 修复闭环）
└── references/
    ├── analysis-protocol.md        # 4 问分析协议（可复现裁决）
    └── report-template.md          # 记分卡模板
```

## 许可

MIT
