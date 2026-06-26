---
name: skill-scoreboard
description: >
  技能使用积分榜 v1.3 — OpenClaw 技能使用追踪与积分管理系统。
  
  触发场景：
  (1) 用户询问技能使用榜单、积分统计（日榜/周榜/月榜/年榜/总榜）
  (2) 用户要求查看技能调用记录、错误日志
  (3) 用户要求查看某技能的使用详情
  (4) 用户要求生成每日/历史积分报告
  (5) 用户询问"今天情况如何"、"工作流复盘"
  
  核心功能：
  - 支持日榜、周榜、月榜、年榜、总榜五种榜单模式
  - 每次技能调用自动记录积分 (+1 * 调用时间秒/权重)
  - 记录调用结果和错误日志
  - 根据技能文件复杂度计算权重（归一化到0.95~0.9975，差距≤5%）
  - 每日定时生成积分榜单快照
  - 每日定时复盘：找出积分冠军技能并固化最佳工作流
  - 支持实时查询当前榜单和历史数据
  
  优先级：第一级（最高优先级）
---

# 技能使用积分榜

## 概述

本技能用于追踪和记录 OpenClaw 中所有技能的使用情况，并根据调用时长和复杂度计算积分。

## 积分规则

```
积分 = 1 × (调用时间秒 / 技能复杂度权重)
```

**复杂度权重**由技能文件的规模决定（归一化到 [0.95, 0.9975]）：
- 最小权重：0.9500
- 最大权重：0.9975
- 任意两技能权重差距 ≤5%
- 计算方式：原始分数 → 对数缩放 → min-max 归一化

**权重越高，相同时间获得的积分越少**（复杂技能调用成本更高）

## 文件结构

```
skill-scoreboard/
├── SKILL.md                      # 本文档
└── scripts/
    └── score_tracker.py          # 核心追踪脚本
```

## 使用方式

### 1. 手动记录技能调用

```bash
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py record \
  --skill <技能名> \
  --duration <调用时长(秒)> \
  --success <true|false> \
  --error <错误信息(可选)>
```

### 2. 查询各类榜单

| 榜单类型 | 命令 | 说明 |
|---------|------|------|
| 今日榜 | `today` | 当天技能调用排名 |
| 本周榜 | `week` | 最近7天技能调用排名 |
| 本月榜 | `month` | 当月技能调用排名 |
| 本年榜 | `year` | 当年技能调用排名 |
| 总榜 | `leaderboard` | 历史累计积分排名 |

```bash
# 今日榜单
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py today

# 本周榜单
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py week

# 本月榜单
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py month

# 本年榜单
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py year

# 总榜（历史）
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py leaderboard --limit 10
```

### 4. 生成每日快照

```bash
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py daily
```

### 5. 查看技能详情

```bash
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py detail --skill <技能名>
```

### 6. 查看所有技能权重

```bash
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py weight
```

### 7. 每日工作流复盘报告

```bash
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py review
```

## 定时任务

用户可通过 OpenClaw cron 功能设置每日定时执行：

```bash
# 每日23:00自动执行
openclaw cron add \
  --name "每日技能积分榜复盘" \
  --schedule "0 23 * * *" \
  --tz "Asia/Shanghai" \
  -- python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py daily && \
     python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py review
```

## 数据存储

| 文件/目录 | 内容 |
|-----------|------|
| `~/.skill_scoreboard/scores.json` | 所有技能的积分数据 |
| `~/.skill_scoreboard/logs/calls.log` | 调用日志 |
| `~/.skill_scoreboard/logs/errors.log` | 错误日志 |
| `~/.skill_scoreboard/daily/` | 每日快照目录 |

## 使用示例

**场景1：用户问"今天用了哪些技能"**
```bash
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py today
```

**场景2：用户问"哪个技能最常用"**
```bash
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py leaderboard --limit 5
```

**场景3：用户问"xia-zhua-zhua 用得怎么样"**
```bash
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py detail --skill xia-zhua-zhua
```

**场景4：用户想看完整的历史统计**
```bash
python3 ~/SharedSkills/skill-scoreboard/scripts/score_tracker.py leaderboard --limit 20
```
