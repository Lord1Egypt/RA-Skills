# 追忆 — 本地语义记忆搜索

> "记忆是我们随身携带的图书馆。" — 普鲁斯特

## 概述

「追忆」是一个完全本地化的记忆搜索技能，基于 BM25 + 多维信号融合，无需任何外部 API 或模型依赖。

适用于：从工作区记忆文件中快速检索相关内容，定位特定决策、配置或历史记录。

## 工作原理

### 架构

```
用户查询 → BM25粗排 → 多维信号重排 → 同文件去重 → Top结果
```

### 搜索信号（五路融合）

| 信号 | 权重 | 作用 |
|------|------|------|
| BM25norm | 38% | 基础词频相关性 + 文档长度归一化 |
| IDF-Coverage | 22% | query 端归一化，解决长文档压垮短查询问题 |
| N-gram Proximity | 20% | 词序/邻近度，区分散落命中与紧密相关 |
| ExactPhrase | 12% | 完整子串 bonus，精准匹配时触发 |
| Soft Dice | 10% | 编辑距离容错，捕捉近似匹配 |

另有连续匹配（Consecutive）和同文件去重作为辅助信号。

### 分词方案

- **英文/数字**：`[a-zA-Z0-9_\-\.]+`
- **中文**：CJK 字符 2-6 gram（适应 Python 3.13 环境，替代 jieba）
- **Query 扩展**：自动生成 bigram，长词优先匹配

## 文件结构

```
追忆/
├── SKILL.md       # 技能定义
├── README.md       # 本文档
└── scripts/
    └── search.py  # 搜索脚本（含索引构建）
```

## 使用方法

### 首次使用：构建索引

```bash
python3 ~/.openclaw/workspace/skills/追忆/scripts/search.py --build
```

索引路径：`~/.openclaw/memory_bm25_index.json`（约 5 MB）

### 搜索

```bash
python3 ~/.openclaw/workspace/skills/追忆/scripts/search.py "查询内容"
```

### 示例

```bash
# 搜索关于年余 GitHub 的记忆
python3 ~/.openclaw/workspace/skills/追忆/scripts/search.py "年余 GitHub"

# 搜索墨尘相关内容
python3 ~/.openclaw/workspace/skills/追忆/scripts/search.py "墨尘"

# 搜索心跳机制
python3 ~/.openclaw/workspace/skills/追忆/scripts/search.py "心跳 机制"
```

### 搜索范围

默认覆盖：
- `~/.openclaw/workspace/MEMORY.md`
- `~/.openclaw/workspace/memory/*.md`

如需添加其他路径，编辑 `search.py` 中的 `MEMORY_PATHS` 列表。

### 调整输出数量

修改 `search.py` 中的 `TOP_K = 8`（默认返回 8 条结果）。

### 重建索引

当记忆文件发生变更时，重新运行 `--build` 即可增量更新（会完全重建索引）。

## 依赖

- Python 3.13+
- 标准库：re, collections, json, math, glob, os, sys

**零外部依赖**，纯 stdlib 实现。

## 版本历史

| 版本 | 更新内容 |
|------|---------|
| v7 | 长词优先匹配 + Dice Coefficient |
| v6 | 同文件去重 + 连续匹配加分 |
| v5 | ExactPhrase + SoftMatch |
| v4 | N-gram Proximity |
| v3 | IDF-Coverage + RRF |
| v2 | BM25 归一化 + 位置衰减 |
| v1 | BM25 基础版 |

## 设计理念

「追忆」的设计遵循以下原则：

1. **不猜语义**：纯统计方法，不依赖语言模型
2. **不差空间**：以搜索质量优先，5 MB 索引可接受
3. **查询即所得**：无需预处理，所见即所搜
4. **结果可解释**：每条结果附带详细信号分值
