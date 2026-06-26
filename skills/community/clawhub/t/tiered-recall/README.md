# 🧠 Tiered Recall - 分层回忆系统

> 解决大模型上下文长度限制，保持跨会话项目延续性。

[![version](https://img.shields.io/badge/version-1.2.2-blue)](./SKILL.md)
[![license](https://img.shields.io/badge/license-MIT-green)](#)
[![author](https://img.shields.io/badge/author-davidme6-orange)](https://github.com/davidme6)

---

## 这是什么

Tiered Recall 是一套给 AI 助手使用的分层回忆系统。

它的目标不是把所有历史一次性塞回上下文，而是把记忆拆成四层，优先加载最关键、最近期、最活跃的部分，让助手在新会话里更快恢复状态。

---

## 解决的问题

大模型上下文有限，复杂项目跨多天、多窗口后，新 session 很容易失去连续性。

常见问题：
- 新开窗口，之前的项目背景全部丢失
- 跨天任务，第二天不记得昨天做了什么
- 多项目并行，切换时上下文混乱
- 手动翻日志太慢，恢复成本高

---

## 四层自动加载

| 层级 | 内容 | Token 预算 | 加载条件 |
|------|------|-----------|----------|
| 🔴 L0 核心 | `MEMORY.md` | ~4k | 始终加载 |
| 🟠 L1 近期 | 最近 7 天日志 | ~10k | 始终加载 |
| 🟡 L2 项目 | 活跃项目文件 | ~5k | 自动检测 |
| 🟢 L3 索引 | 记忆索引 | ~3k | 始终加载 |
| **总计** | | **~22k** | 默认可控 |

说明：
- 默认自动加载最近 7 天，可在 `config.json` 里修改
- 手动回忆时支持全量加载或自定义天数

---

## v1.2.2 的稳定点

这个版本保留了 `v1.2.0` 之后的自动 7 天和手动全量/自定义天数能力，同时保留索引瘦身后的稳定实现。

当前实现的 `slim index` 只存：
- 文件名
- 行号
- 标题

不再把摘要文本写进索引，避免 L3 token 膨胀。

---

## 重要 Bug 修复

`v1.1.0` 的索引把摘要也写进了 L3，导致索引体积明显膨胀。

`v1.2.0+` 改成 slim index 后：
- 索引不再存摘要
- L3 预算回到可控范围
- 保留定位能力，方便按主题、项目和日期回忆

代码层面的索引条目现在是：

```json
{
  "f": "2026-04-24.md",
  "l": "120-168",
  "t": "项目推进"
}
```

---

## 文件结构

```text
workspace/
├── MEMORY.md
├── memory/
├── .tiered-recall/
│   ├── index.json
│   ├── projects.json
│   └── state.json
└── skills/tiered-recall/
    ├── SKILL.md
    ├── README.md
    ├── config.json
    └── scripts/
```

---

## 使用方式

### 自动加载

默认新 session 会加载：
1. `MEMORY.md`
2. 最近 7 天日志
3. 活跃项目
4. 记忆索引

### 手动回忆

常见指令：

| 指令 | 作用 |
|------|------|
| `回忆全部` | 加载全部记忆 |
| `回忆最近14天` | 加载最近 N 天日志 |
| `回忆 [项目名]` | 加载项目相关记忆 |
| `回忆 [日期]` | 加载指定日期日志 |
| `回忆 [关键词]` | 按主题或关键词搜索 |

### 脚本

```bash
# 重建索引
python skills/tiered-recall/scripts/build-index.py

# 默认加载（最近7天）
python skills/tiered-recall/scripts/load.py

# 全量加载
python skills/tiered-recall/scripts/load.py --full

# 自定义天数
python skills/tiered-recall/scripts/load.py --days 14
```

---

## 与 Jarvis Core 的关系

`tiered-recall` 是 `jarvis-core` 的依赖项。

当 `jarvis-core` 需要在新会话里恢复记忆、项目状态和关系上下文时，会把它当作底层记忆加载层来使用。

---

## 配置

`config.json` 当前核心配置：

```json
{
  "recentDays": 7,
  "maxTokensPerLayer": {
    "L0": 4000,
    "L1": 10000,
    "L2": 5000,
    "L3": 3000
  },
  "deepRecallBudget": 50000,
  "autoLoadOnNewSession": true
}
```

---

## Changelog

### v1.2.2
- 保留自动 7 天加载
- 保留 `--full` 和 `--days N`
- 保留 slim index bugfix 实现
- 同步到独立 GitHub 仓库和 ClawHub

### v1.2.0
- 修复 L3 索引 token 膨胀问题
- 改成 slim index

### v1.1.0
- 增加 10 字摘要

### v1.0.0
- 初始版本

---

**Made with 🧠 by [davidme6](https://github.com/davidme6)**
