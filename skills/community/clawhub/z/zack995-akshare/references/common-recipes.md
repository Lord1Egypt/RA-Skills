# AKShare common recipes

Run these via `{baseDir}/scripts/akshare_eval.py` with the Python inside your AKShare venv.

Typical command shape:

```bash
$HOME/.openclaw/.venvs/akshare/bin/python {baseDir}/scripts/akshare_eval.py --expr "..."
```

If you installed to a custom venv, replace the Python path accordingly.

## A股历史行情

```bash
--expr "ak.stock_zh_a_hist(symbol='000001', period='daily', start_date='20240101', end_date='20240131', adjust='')"
```

## A股实时行情（全市场，结果较大）

```bash
--expr "ak.stock_zh_a_spot_em()"
```

## 交易日历

```bash
--expr "ak.tool_trade_date_hist_sina()"
```

## ETF 实时行情

```bash
--expr "ak.fund_etf_spot_em()"
```

## 宏观：中国 LPR

```bash
--expr "ak.macro_china_lpr()"
```

## 国债收益率

```bash
--expr "ak.bond_zh_us_rate()"
```

## 指数历史行情

```bash
--expr "ak.index_zh_a_hist(symbol='000001', period='daily', start_date='20240101', end_date='20240131')"
```

## 注意

- 不同接口参数名不完全一致，先用最小范围测试。
- 脚本默认输出前 N 行 CSV；需要结构化时加 `--format json`。
- 如果上游站点改版，接口可能临时失效，需要换同类接口。
