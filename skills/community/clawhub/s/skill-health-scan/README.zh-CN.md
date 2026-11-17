# 🩺 Skill Health Checkup

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**[English](README.md)** | **中文**

给你已安装的全部技能做一次全面体检：谁和谁触发重叠、谁从不被唤醒、谁的描述有缺陷——一份带具体修复建议的健康报告。

**5 项检查。1 份报告。0 依赖。**

**解决的痛点**：技能装多了会互相打架——同一句话唤醒两个技能、真正重要的场景反而没人响应、模糊的描述让技能变成死重。等 agent 误触发时才发现就晚了，Skill Health Checkup 帮你提前查出来。

## 目录

<details>
<summary>点击展开</summary>

- [工作原理](#工作原理)
- [五项检查](#五项检查)
- [安装](#安装)
- [快速开始](#快速开始)
- [文件结构](#文件结构)
- [许可](#许可)

</details>

## 工作原理

```
skills 目录 ──▶ scan_skills.py ──▶ 名称 / 描述 / 关键词
                     │
                     ▼
        ┌──── Agent 语义体检 ────┐
        │  触发重叠配对           │
        │  盲区 · 描述健康度      │
        │  重复 · 死重            │
        └──────────┬─────────────┘
                   ▼
        🩺 健康报告 + 前三大修复
```

脚本负责确定性事实（解析 frontmatter、提取触发短语、关键词重叠预筛），Agent 做语义层面的红/黄/绿判定并给出精确的描述修改建议。

## 五项检查

| # | 检查 | 捕捉什么 |
|---|---|---|
| 1 | **触发重叠** | 两个技能声称同一场景——并引用能同时唤醒它们的那句话 |
| 2 | **盲区** | 高频任务没有技能覆盖——附一句式的扩展思路 |
| 3 | **描述健康度** | 过短 / 没有 "Use when" 触发短语 / 只写功能不写场景 |
| 4 | **重复安装** | 同一功能装了两份 |
| 5 | **死重** | 从不触发还很大（引用文件多）的技能——白占加载成本 |

## 安装

```bash
# ClawHub
clawhub install skill-health-scan

# 或从源码
git clone https://github.com/Thomaszhou22/skill-health-scan.git
cp -r skill-health-scan ~/.openclaw/skills/
```

## 快速开始

```bash
# 1. 确定性扫描
python3 scripts/scan_skills.py --dir ~/.openclaw/skills --json

# 2. 对 Agent 说："跑一次技能体检"
```

## 文件结构

```
skill-health-scan/
├── SKILL.md                    # 体检流程（5 项检查 + 修复协议）
├── scripts/
│   └── scan_skills.py          # 确定性扫描器（纯标准库）
└── references/
    └── report-template.md      # 健康报告模板
```

## 许可

MIT
