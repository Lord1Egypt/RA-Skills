---
name: tavily-search
description: >
  Enhanced Tavily web search for fact-checking and cross-verification.
  Aligned with official Tavily API (2026-03). Supports time_range, exact_match,
  domain filtering, finance topic. Use for verifying Scout research results.
tags: [search, web, fact-check, tavily, verification]
platforms: [Claude, Gemini]
allowed-tools: [Bash]
---

# Tavily Search (Enhanced)

AI-optimized web search via [Tavily API](https://tavily.com). Enhanced version with full official API parameter support.

**主要用途**: 交叉验证 Scout 调研结果的事实准确性，而非替代 Scout 做调研。

## Usage

```bash
node {baseDir}/scripts/search.mjs "query" [options]
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `-n <count>` | Max results (1-20) | 5 |
| `--deep` | Advanced search (更准确，2 credits) | basic |
| `--topic <t>` | `general` \| `news` \| `finance` | general |
| `--time-range <r>` | `day` \| `week` \| `month` \| `year` | 无限制 |
| `--start-date <d>` | YYYY-MM-DD (结果起始日期) | — |
| `--end-date <d>` | YYYY-MM-DD (结果截止日期) | — |
| `--include-domains <d>` | 逗号分隔，限定搜索域名 | — |
| `--exclude-domains <d>` | 逗号分隔，排除域名 | — |
| `--exact` | 精确匹配引号内短语 | false |
| `--country <name>` | 提升特定国家结果 (china/united states/japan) | — |
| `--images` | 包含图片结果 | false |
| `--raw` | 包含页面原始 markdown 内容 | false |
| `--json` | 输出原始 JSON（供脚本消费） | false |

## Fact-Check Examples

**验证某个具体事实**:
```bash
node {baseDir}/scripts/search.mjs "武侯祠 建于哪一年" --exact --include-domains baike.baidu.com,zh.wikipedia.org -n 3
```

**验证最新新闻**:
```bash
node {baseDir}/scripts/search.mjs "成都大庙会 2026" --topic news --time-range month -n 5
```

**验证金融数据**:
```bash
node {baseDir}/scripts/search.mjs "MiniMax 融资 估值" --topic finance --time-range year
```

**深度调研 + 限定来源**:
```bash
node {baseDir}/scripts/search.mjs "川剧变脸 历史 起源" --deep --country cn -n 10
```

## When To Use

- ✅ **Scout 返回的调研结果** → 用 Tavily 交叉验证关键事实
- ✅ **推文/内容生产** → 验证引用的数据、日期、名称是否准确
- ✅ **时效性信息** → `--topic news --time-range week` 获取最新
- ❌ **不要用于替代 Scout 做全面调研** — Scout 有更完整的搜索+分析能力

## vs Upstream tavily-search

| Feature | Upstream | This version |
|---------|----------|-------------|
| time_range / start_date / end_date | ❌ (deprecated `days`) | ✅ |
| include_domains / exclude_domains | ❌ | ✅ |
| exact_match | ❌ | ✅ |
| finance topic | ❌ | ✅ |
| country boost | ❌ | ✅ |
| include_images | ❌ | ✅ |
| raw content (markdown) | ❌ | ✅ |
| JSON output mode | ❌ | ✅ |
| const/require bugs | ⚠️ 2 bugs | ✅ Fixed |
| Response timing | ❌ | ✅ |

## Environment

- `TAVILY_API_KEY` env var, or in `~/.openclaw/.env` / `~/.env`
- Cost: 1 credit (basic) / 2 credits (advanced/deep)
