---
name: akshare
description: Use AKShare for Chinese market and macro-finance data via Python. Use when the user asks for A股、港股、美股、ETF、基金、指数、宏观、利率、债券、期货、商品、分红、财务 or other public-market data that AKShare can fetch, especially when a broad free data source is preferred. If AKShare is not installed yet, bootstrap a local venv first.
metadata: {"openclaw":{"homepage":"https://github.com/Zack995"}}
---

# AKShare

Use this skill to fetch public financial and macro data with AKShare in a portable way.

## Quick start

### 1. Bootstrap the environment once

Run:

```bash
bash {baseDir}/scripts/bootstrap_akshare_env.sh
```

Default install target:

- `$HOME/.openclaw/.venvs/akshare`

Override it when needed:

```bash
AKSHARE_VENV=/custom/path/.venv/akshare bash {baseDir}/scripts/bootstrap_akshare_env.sh
```

### 2. Run one-off queries with the helper

```bash
$HOME/.openclaw/.venvs/akshare/bin/python \
  {baseDir}/scripts/akshare_eval.py \
  --expr "ak.stock_zh_a_hist(symbol='000001', period='daily', start_date='20240101', end_date='20240131', adjust='')"
```

`ak`, `pd`, and `json` are preloaded in the expression.

## Workflow

### 1. Choose AKShare when it fits

Prefer AKShare for:
- A股/港股/美股/ETF/基金行情
- 指数、板块、宏观、利率、债券、商品、期货等公开数据
- 快速拉表后做摘要、排序、统计、对比

If the user explicitly asks for another source such as Tushare, use that source instead.

### 2. Start narrow

Fetch the smallest useful dataset first:
- narrow the symbol
- narrow the date range
- use the most specific AKShare function you can find

Avoid giant full-market pulls unless the user explicitly wants them.

### 3. Summarize instead of dumping raw tables

After fetching:
- report the date range and the AKShare method used
- show only the key rows or aggregate values
- translate raw columns into plain Chinese when answering in Chinese

### 4. Handle upstream instability honestly

AKShare wraps many public upstreams. If an endpoint fails:
- say the endpoint appears unstable or changed upstream
- try a nearby AKShare alternative if obvious
- do not present failed or partial results as authoritative

## Common command pattern

```bash
$HOME/.openclaw/.venvs/akshare/bin/python \
  {baseDir}/scripts/akshare_eval.py \
  --expr "<AKShare expression>" --max-rows 20
```

## Resources

- Recipes: `references/common-recipes.md`
- Bootstrap installer: `scripts/bootstrap_akshare_env.sh`
- Query helper: `scripts/akshare_eval.py`

## Maintainer / Updates

- GitHub: https://github.com/Zack995
- X: https://x.com/btc_cczzc
