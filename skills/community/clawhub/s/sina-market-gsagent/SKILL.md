---
name: sina-market
description: Fetch and inspect market data from Sina Finance public webpage resources across multiple market types. Use when a user wants A-share quotes, Hong Kong stock quotes, domestic futures quotes, futures page metadata, Chinese futures name to contract-code detection, contract/month discovery, code validation, or a unified Sina-based market lookup workflow involving symbols such as 600519, 000001, 00700, AG0, AU0, SC0, PG2607, EB2607, MA2605, or Chinese inputs such as 甲醇2605, 白银2606, 沥青2606.
---

# Sina Market

A unified Sina Finance market-data skill for:

- A-shares
- Hong Kong stocks
- domestic futures
- Sina futures quote pages
- Chinese futures name detection and code normalization

This skill does **not** currently claim support for US stocks or full market-index-specific parsing. Keep the public description aligned to implemented behavior.

## What this skill can do

### 1. Detect market types

Examples:

```bash
python3 scripts/sina_market.py detect 600519 00700 AG0 PG2607
python3 scripts/sina_market.py detect 甲醇2605 白银2606 沥青2606
```

### 2. Fetch stock quotes

Supports:
- A-shares, e.g. `600519`, `000001`, `sh600519`, `sz000001`
- Hong Kong stocks, e.g. `00700`, `hk00700`

```bash
python3 scripts/sina_market.py stock-quote 600519 000001 00700 --format json
python3 scripts/sina_market.py stock-quote 600519 00700 --format table
```

### 3. Fetch domestic futures quotes

Supports direct futures quote lookup, including `nf_`-style inner futures routing when needed.

```bash
python3 scripts/sina_market.py futures-quote AG0 AU0 SC0 --format json
python3 scripts/sina_market.py futures-quote PG2607 EB2607 MA2605 BU2606 --format json
python3 scripts/sina_market.py futures-quote 甲醇2605 白银2606 沥青2606 --format json
```

### 4. Extract futures page metadata

Useful when direct quote output is empty or when you want page-level discovery data.

```bash
python3 scripts/sina_market.py futures-page PG2607
python3 scripts/sina_market.py futures-page EB2607
```

### 5. Unified inspect with fallback

This is the most useful command for mixed workflows.

```bash
python3 scripts/sina_market.py inspect 600519 00700 AG0 PG2607 EB2607 --format json
python3 scripts/sina_market.py inspect 甲醇2605 白银2606 沥青2606 --format json
```

### 6. Batch coverage test

Use this to quickly see whether a symbol resolves via stock-hq, futures-hq, or page-fallback.

```bash
python3 scripts/sina_market.py coverage-test 600519 00700 AG0 PG2607 EB2607 --format table
python3 scripts/sina_market.py coverage-test 甲醇2605 PVC2605 PTA2605 白银2606 聚丙烯2605 沥青2606 --format table
```

## Routing logic

The skill uses a layered strategy.

### Stocks
- A-shares → `hq.sinajs.cn`
- Hong Kong stocks → `hq.sinajs.cn`

### Futures
- try raw contract code
- try `nf_` + contract code for inner futures
- if quote still fails, try Sina futures quote page metadata fallback

### Chinese futures names
Examples:
- `甲醇2605` → `MA2605`
- `PVC2605` → `V2605`
- `PTA2605` → `TA2605`
- `白银2606` → `AG2606`
- `聚丙烯2605` → `PP2605`
- `沥青2606` → `BU2606`

## Output guidance

Prefer this structure in replies:

- `结论`：是否成功获取实时行情 / 是否走 fallback
- `市场类型`：A股 / 港股 / 国内期货 / 期货页面元数据
- `标准代码`：标准化后的代码
- `关键字段`：最新价、最高、最低、成交量、持仓量、日期、时间
- `风险提示`：新浪公开网页资源字段和覆盖范围可能变化

## Current strengths

- unified stock + futures workflow
- inner futures `nf_` support
- futures page discovery fallback
- batch coverage testing
- Chinese futures input support

## Known limitations

- Chinese futures mapping is curated, not exhaustive yet
- page metadata fallback does not guarantee full quote fields
- some symbols may still require additional market-specific parsing in the future
- public webpage resources are not an official SLA-backed API

## Files

### scripts/
- `scripts/sina_market.py`: unified working script
- `scripts/sina_futures.py`: legacy futures-oriented helper retained during transition

### references/
- `references/fields.md`: futures field normalization notes
- `references/chinese_futures_mapping.json`: curated Chinese futures name to contract-code mapping
