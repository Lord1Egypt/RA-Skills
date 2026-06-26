---
name: 追忆
description: 本地记忆语义搜索。当用户查询记忆、搜索过往记录、询问"我记得..."、"搜一下..."等所有记忆召回场景时触发。基于 BM25 + 多维信号融合，完全本地运行，无需 API Key。
---

# 追忆 — 本地语义记忆搜索

> "记忆是我们随身携带的图书馆。" — 普鲁斯特

## 快速开始

搜索记忆：
```bash
python3 ~/.openclaw/workspace/skills/追忆/scripts/search.py "查询内容"
```

构建/更新索引：
```bash
python3 ~/.openclaw/workspace/skills/追忆/scripts/search.py --build
```

## 搜索流程

当用户发起记忆搜索时：

1. **检查索引是否存在** — 索引路径 `~/.openclaw/memory_bm25_index.json`
2. **如无索引，先构建** — 调用 `--build` 生成索引
3. **执行搜索** — BM25 粗排 → 多维信号重排 → 同文件去重
4. **格式化输出** — 返回文件路径、行号、各信号分值、内容摘要

## 搜索信号

| 信号 | 权重 | 说明 |
|------|------|------|
| BM25norm | 38% | 词频相关性 + 文档长度归一化 |
| IDF-Coverage | 22% | query 端归一化 |
| N-gram Proximity | 20% | 词序/邻近度 |
| ExactPhrase | 12% | 完整子串 bonus |
| Soft Dice | 10% | 编辑距离容错匹配 |

## 索引范围

- `MEMORY.md`
- `memory/*.md`（每日日记）

## 搜索结果格式

```
🔍 搜索: 年余 GitHub

[1] 综合: 0.800
    BM25n: 1.000  Cover: 1.000  Prox: 1.000  Phrase: 0.000  Soft: 0.000  Consec: 0.000
    来源: memory/2026-04-03.md#165-181
    内容: ...相关段落内容...

[2] 综合: 0.788 [去重]
    ...
```

## 触发时机

以下场景自动触发本 Skill：
- 用户说"搜一下我记得的 XXX"
- 用户说"我的记忆里有关于 XXX 的吗"
- 用户询问"之前我们聊过 XXX"
- 用户说"查一下 XXX 相关的内容"
- 任何 `memory_search` 工具调用

## 技术细节

- **分词**：CJK 字符 2-6 gram（Python 3.13 兼容，无外部依赖）
- **排序算法**：BM25（k1=1.5, b=0.75）+ 五路信号融合
- **索引格式**：JSON，每条记录含 text / file / start_line / end_line / chunk_idx
- **零外部依赖**：全部使用 Python stdlib
