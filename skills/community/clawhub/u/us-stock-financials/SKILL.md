---
name: us-stock-financials
description: Fetch comprehensive financial data from SEC EDGAR XBRL for US-listed companies (especially Chinese ADRs). Includes balance sheet, income statement, cash flow, per-share metrics, and PDF report generation.
---

# US Stock Financials

从 SEC EDGAR 获取全面的财务数据并生成 PDF 报表。

## 数据范围

### 资产负债表
- 总资产、流动/非流动资产
- 现金及等价物、应收账款、存货、固定资产、商誉
- 总负债、流动/非流动负债
- 应付账款、短期/长期借款
- 股东权益、留存收益

### 利润表
- 营业收入、营业成本、毛利润
- 研发费用、销售及管理费用
- 营业利润、利息支出、所得税、净利润

### 现金流量表
- 经营/投资/融资活动现金流
- 资本支出、收购支出

### 每股指标
- 基本/稀释每股收益
- 每股股息

## 使用方法

```bash
# 搜索公司并获取财务数据
python3 scripts/sec_finance.py --search JD.com

# 获取季度数据
python3 scripts/sec_finance.py --search Alibaba --period quarterly

# 生成 PDF 报表
python3 scripts/sec_finance.py --search JD.com --pdf /tmp/jd_report.pdf

# JSON 输出
python3 scripts/sec_finance.py --search PDD --output json
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--search` | 公司名称、股票代码或别名 |
| `--cik` | SEC CIK 编号 (10位) |
| `--period` | annual / quarterly / all |
| `--output` | table / json |
| `--pdf` | 生成 PDF 报表路径 |

## 内置公司

京东(JD)、阿里巴巴(BABA)、百度(BIDU)、拼多多(PDD)、哔哩哔哩(BILI)、微博(WB)、贝壳(BEKE) 等中概股。

## 依赖

- Python 3.8+
- reportlab (PDF生成): `pip3 install reportlab --break-system-packages`
