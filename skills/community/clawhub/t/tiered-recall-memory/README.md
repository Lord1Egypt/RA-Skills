# Tiered Recall 🧠📚

**分层回忆系统 - 解决大模型上下文长度限制，保持项目延续性**

[![ClawHub](https://img.shields.io/badge/ClawHub-tiered--recall-blue)](https://clawhub.com/skill/tiered-recall)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://clawhub.com/skill/tiered-recall)

---

## 🎯 核心问题

大模型上下文有限（约20万token），复杂项目可能跨多天、多窗口进行。每次新session开始时，如何快速恢复上下文，保持工作延续性？

**常见痛点：**
- 新开窗口，之前的项目背景丢失
- 跨天任务，第二天不记得昨天做了什么
- 多项目并行，切换时混乱
- 手动回顾太慢，浪费时间

---

## 🚀 解决方案

### 分层加载策略

| 层级 | 内容 | Token预算 | 加载条件 |
|------|------|-----------|----------|
| 🔴 L0 核心 | `MEMORY.md` | ~4k | 始终加载 |
| 🟠 L1 近期 | 最近2天日志 | ~10k | 始终加载 |
| 🟡 L2 项目 | 活跃项目文件 | ~5k | 自动检测 |
| 🟢 L3 索引 | 记忆索引 | ~1k | 始终加载 |
| **总计** | | **~20k** | |

---

## 📦 安装

```bash
clawhub install tiered-recall
```

---

## 🔧 使用方法

### 1. 生成索引

```bash
python skills/tiered-recall/scripts/build-index.py
```

### 2. 加载记忆

```bash
# 默认分层加载
python skills/tiered-recall/scripts/load.py

# 按项目加载
python skills/tiered-recall/scripts/load.py --project "搞钱特战队"

# 按主题加载
python skills/tiered-recall/scripts/load.py --topic "游戏开发"
```

### 3. 手动深度回忆

在对话中使用：
- `继续回忆` - 加载更多相关记忆
- `回忆 [项目名]` - 加载该项目全部记忆
- `回忆 [天数]` - 加载指定天数日志
- `回忆 [关键词]` - 按关键词搜索记忆

---

## 📂 文件结构

```
workspace/
├── MEMORY.md              # L0 核心记忆
├── memory/                # L1 每日日志
│   ├── 2026-03-25.md
│   └── 2026-03-24.md
├── .tiered-recall/        # 索引和状态
│   ├── index.json         # 记忆索引
│   └── projects.json      # 活跃项目
└── skills/
    └── tiered-recall/
        ├── SKILL.md
        ├── README.md
        ├── config.json
        └── scripts/
            ├── build-index.py
            └── load.py
```

---

## 📈 效果

| 场景 | 无分层回忆 | 有分层回忆 |
|------|-----------|-----------|
| 新session启动 | 手动回顾5-10分钟 | 自动加载，即刻恢复 |
| 跨天任务 | "我们昨天做什么来着" | "继续昨天的X任务" |
| 多项目切换 | 混乱、遗忘 | 自动加载项目上下文 |
| Token消耗 | 随机、不稳定 | 可控、~20k预算 |

---

## 📝 Changelog

### v1.0.0 (2026-03-25)
- ✨ 初始版本
- 🔄 支持分层自动加载
- 🔍 支持手动深度回忆
- 📊 Token预算控制
- 🗂️ 记忆索引生成

---

## 👤 Author

**davidme6**
- GitHub: https://github.com/davidme6
- ClawHub: https://clawhub.com/skill/tiered-recall

---

## 📄 License

MIT License