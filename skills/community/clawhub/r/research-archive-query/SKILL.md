---
name: research-archive-query
description: 统一查询本地研究资料库，默认同时搜索 AlphaPai 归档和 knowledge_bases，支持精确检索、向量检索和混合检索，并默认排除 private 资料库如 personal。
---

# Research Archive Query

这个 skill 用来统一查询你本地已经归档好的研究资料。

默认覆盖：

1. `alphapai` 归档点评库
2. `knowledge_bases` 归档资料库

默认行为：

- 这是查询 skill，不负责抓取；请先有 `alphapai-scraper` 或 `knowledge-base` 产生的本地归档
- 默认查询最近 `7` 天
- 默认使用 `hybrid` 模式，同时跑精确检索和向量召回
- 默认不查询 private scope，例如 `personal`
- 输出一份适合手机阅读的检索摘要

## 何时使用

- 用户说“根据本地研究资料库查最近一周英伟达更新”
- 用户要把 `alphapai + knowledge_bases` 的命中结果统一汇总
- 用户要明确排除 `personal` 之类 private 资料库
- 用户要按最近几天、某个行业、某个标的做统一检索

## 运行方式

默认统一查询：

```bash
python3 /Users/bot/.openclaw/workspace/skills/research-archive-query/scripts/unified_query.py --query 英伟达 --days 7 --mode hybrid
```

如果用户明确要求只做精确检索：

```bash
python3 /Users/bot/.openclaw/workspace/skills/research-archive-query/scripts/unified_query.py --query 英伟达 --days 7 --mode exact
```

如果用户明确要求只做语义模糊检索：

```bash
python3 /Users/bot/.openclaw/workspace/skills/research-archive-query/scripts/unified_query.py --query 英伟达 --days 7 --mode vector
```

如果用户明确说只查某个来源，可以加：

```bash
--sources alphapai
```

或：

```bash
--sources knowledge_bases
```

如果用户明确要求把 private 库也算进去，才追加：

```bash
--include-private
```

## 输出

- 摘要：`~/.openclaw/data/research-archive-query/reports/YYYYMMDD_HHMMSS_unified_query.md`
- 元数据：`~/.openclaw/data/research-archive-query/runtime/YYYYMMDD_HHMMSS_unified_query.json`

## 使用规则

- 如果用户没有指定天数，默认 `7` 天
- 如果用户说“最近一周”，用 `--days 7`
- 如果用户说“最近一个月”，用 `--days 30`
- 如果用户没指定模式，默认 `--mode hybrid`
- 如果用户没明确授权，不要加 `--include-private`

## 当前接入范围

当前已接入：

- `alphapai`
- `knowledge_bases`

后续如果新增归档仓库，保持相同归档思路后，只需要在 `scripts/registry.py` 增加一个 adapter。
