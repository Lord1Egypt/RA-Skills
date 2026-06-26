---
name: stock-deep-analysis
description: 美股/港股/A股深度财务分析报告生成工具。输入股票代码，自动从 Yahoo Finance（Tushare for A股）拉取财务报表、估值、行情数据，生成结构化 Markdown 分析报告。支持 PDD/KC/任意 ticker。
version: 1.0.0
tags:
  - finance
  - stock-analysis
  - yfinance
  - investment
dependency:
  python:
    - yfinance>=0.2.40
environment:
  TUSHARE_TOKEN: A股专用（Tushare token），美股不需要
triggers:
  - 分析股票
  - 深度报告
  - 股票分析
  - PDD分析
  - KC分析
  - 持仓分析
  - 美股分析
  - 港股分析
---

# Stock Deep Analysis（股票深度分析）

## 功能概述

输入股票代码，自动从 Yahoo Finance 拉取数据，生成结构化 Markdown 深度分析报告：

1. **公司概况** — 业务简介、行业、主营业务
2. **估值分析** — PE/PB/PS、52周高低、分析师目标价、EV/EBITDA
3. **盈利能力** — 营收/毛利/净利/ EPS 历史走势
4. **资产负债** — 资产质量、债务结构、流动比率
5. **成长能力** — 营收增速、利润增速、季度环比
6. **现金流** — FCF、经营现金流、资本支出
7. **持仓状态** — 用户成本、盈亏、距52周高低距离
8. **综合结论** — 多空逻辑 + 操作建议

## 前置准备

### 依赖安装

```bash
# 建议用 hermes-agent venv
cd ~/.hermes/hermes-agent/venv
uv pip install yfinance>=0.2.40 --python ./bin/python3

# 验证
~/.hermes/hermes-agent/venv/bin/python3 -c "import yfinance; print('OK:', yfinance.__version__)"
```

### A 股额外依赖（Tushare）

```bash
cd ~/.hermes/hermes-agent/venv
uv pip install tushare>=1.2.80 --python ./bin/python3
```

## 使用方法

### 方式一：命令行直接生成（推荐）

```bash
PYTHON=~/.hermes/hermes-agent/venv/bin/python3

# 美股（Yahoo Finance）
$PYTHON ~/.hermes/skills/stock-deep-analysis/scripts/generate_report.py \
  --ticker PDD --market US

# 港股（Yahoo Finance， ticker 需加 .HK）
$PYTHON ~/.hermes/skills/stock-deep-analysis/scripts/generate_report.py \
  --ticker 0700.HK --market HK

# A股（Tushare，需配置 token）
export TUSHARE_TOKEN="your_token"
$PYTHON ~/.hermes/skills/stock-deep-analysis/scripts/generate_report.py \
  --ticker 600141.SH --market CN
```

### 方式二：传入持仓成本（计算盈亏）

```bash
PYTHON=~/.hermes/hermes-agent/venv/bin/python3

$PYTHON ~/.hermes/skills/stock-deep-analysis/scripts/generate_report.py \
  --ticker PDD --market US --cost 100.0
```

### 方式三：Python 调用

```python
import sys
sys.path.insert(0, '~/.hermes/skills/stock-deep-analysis/scripts')
from generate_report import generate_stock_report

report = generate_stock_report(
    ticker='PDD',
    market='US',       # 'US' | 'HK' | 'CN'
    cost=None,         # 持仓成本（美元/港币/人民币，按市场货币单位）
    currency='USD'     # 'USD' | 'HKD' | 'CNY'（用于成本换算显示）
)
print(report)
```

## 支持的市场

| market | 数据源 | 示例 ticker |
|--------|--------|-----------|
| `US` | Yahoo Finance | `PDD`, `AAPL`, `TSLA`, `KC` |
| `HK` | Yahoo Finance | `0700.HK`, `9988.HK`, `1810.HK` |
| `CN` | Tushare | `600141.SH`, `000001.SZ` |

## 持仓成本说明

- `cost` 参数按 `--market` 对应的货币单位填写
- 美股：美元；港股：港币；A股：人民币
- 不传 `cost` 则只输出分析报告，不计算盈亏

## 输出示例

```
# PDD Holdings（拼多多）深度分析报告

**报告日期：** 2026-05-29 | **当前价：** $82.02 | **成本价：** $100（-18%）

---

## 一、公司基本情况
## 二、估值分析
## 三、财务业绩（Annual）
## 四、资产负债质量
## 五、自由现金流
## 六、持仓状态
## 七、综合结论
```

## 已知问题（Pitfalls）

1. **Yahoo Finance 限流**：高频请求会触发 `429 Too Many Requests`，脚本内置 3 次重试 + 2 秒等待
2. **美股财报货币单位**：yfinance 返回的 EPS/利润数据已是美元单位，无需额外换算
3. **港股 ticker 格式**：必须在 ticker 后加 `.HK`，如 `0700.HK`
4. **A股需配置 Tushare Token**：免费账号 `fina_indicator` 接口限制 1次/分钟，需等待 65 秒以上
5. **信息过老**：美股财报披露后 Yahoo Finance 更新可能延迟 1-2 天

## 文件结构

```
stock-deep-analysis/
├── SKILL.md                        ← 主技能说明
├── scripts/
│   ├── generate_report.py          ← 主脚本（调用 fetch + 生成报告）
│   └── fetch_stock_data.py         ← 数据拉取模块（yfinance/Tushare）
└── references/
    └── indicators-guide.md         ← 财务指标评价标准参考
```