---
name: stock-data-collector
description: 采集A股和港股指定股票的历史数据。支持多股票批量采集、多种时间周期（日线/周线/月线/分钟线）、数据导出为CSV格式。使用场景：(1) "采集贵州茅台和腾讯的历史数据"，(2) "批量采集我的自选股"，(3) "获取某只股票的所有历史数据"。
---

# 股票历史数据采集技能

采集A股和港股指定股票的历史数据，支持批量采集和多周期数据。

## 支持的市场

- **A股**：上海证券交易所（600xxx, 688xxx）、深圳证券交易所（000xxx, 001xxx, 300xxx）
- **港股**：香港联合交易所（0xxxx, 1xxxx, 8xxxx）

## 快速开始

### 单只股票采集

```bash
# A股示例：贵州茅台（600519）
python3 scripts/fetch_stock.py --code 600519 --market A

# 港股示例：京东健康（06618）
python3 scripts/fetch_stock.py --code 06618 --market HK
```

### 批量采集

```bash
# 从列表文件批量采集
python3 scripts/batch_fetch.py --file stock_list.txt

# 命令行指定多只股票
python3 scripts/batch_fetch.py --codes 600519,000001,06618 --markets A,A,HK
```

## 详细用法

### 单只股票采集脚本

```bash
python3 scripts/fetch_stock.py [选项]

选项:
  --code CODE        股票代码（必需）
  --market MARKET    市场：A=A股，HK=港股（必需）
  --period PERIOD    时间周期：daily/weekly/monthly/1min/5min/15min/30min/60min（默认：daily）
  --start DATE       开始日期：YYYYMMDD（默认：20000101）
  --end DATE         结束日期：YYYYMMDD（默认：今天）
  --output DIR       输出目录（默认：./stock_data）
  --name NAME        股票名称（可选，自动获取）
```

示例：
```bash
# 采集贵州茅台日线数据
python3 scripts/fetch_stock.py --code 600519 --market A

# 采集腾讯控股周线数据
python3 scripts/fetch_stock.py --code 00700 --market HK --period weekly

# 采集指定时间范围
python3 scripts/fetch_stock.py --code 600519 --market A --start 20200101 --end 20231231
```

### 批量采集脚本

```bash
python3 scripts/batch_fetch.py [选项]

选项:
  --file FILE        股票列表文件（每行格式：代码,市场,名称）
  --codes CODES      股票代码列表，逗号分隔
  --markets MARKETS  市场列表，逗号分隔（A=A股，HK=港股）
  --names NAMES      股票名称列表，逗号分隔（可选）
  --period PERIOD    时间周期（默认：daily）
  --output DIR       输出目录（默认：./stock_data）
```

示例：
```bash
# 从文件批量采集
python3 scripts/batch_fetch.py --file my_stocks.txt

# 命令行批量采集
python3 scripts/batch_fetch.py --codes 600519,000001,06618 --markets A,A,HK

# 批量采集并指定输出目录
python3 scripts/batch_fetch.py --file my_stocks.txt --output ./my_portfolio_data
```

### 股票列表文件格式

创建一个文本文件，每行一只股票：

```
# my_stocks.txt
# 格式：股票代码,市场,股票名称（名称可选）
600519,A,贵州茅台
000001,A,平安银行
00700,HK,腾讯控股
06618,HK,京东健康
300750,A,宁德时代
```

## 数据源

- **A股数据**：akshare（免费开源）
- **港股数据**：akshare + yfinance

## 数据字段

### A股数据字段
- 日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率

### 港股数据字段
- 日期、开盘、收盘、最高、最低、成交量、成交额（根据数据源可能有所不同）

## 输出格式

所有数据导出为 **CSV 格式**，UTF-8编码，可直接用 Excel、Pandas 等工具打开。

文件命名规则：
```
{股票名称}_{股票代码}_{市场}_{周期}.csv
示例：贵州茅台_600519_A_daily.csv
```

## 依赖安装

```bash
# 安装必需的库
pip install akshare yfinance pandas
```

## 技能文件结构

```
stock-data-collector/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── fetch_stock.py          # 单只股票采集脚本
│   ├── batch_fetch.py          # 批量采集脚本
│   └── example_list.txt        # 股票列表示例
└── examples/                   # 示例文件（可选）
```

## 常见问题

**Q: 如何知道某只股票的代码？**
A: A股600xxx/688xxx是沪市，000xxx/001xxx/300xxx是深市；港股是5位数字。

**Q: 采集失败怎么办？**
A: 检查网络连接，确认股票代码正确。部分港股可能需要用 yfinance 作为备选数据源。

**Q: 数据频率有哪些选项？**
A: 支持 daily（日线）、weekly（周线）、monthly（月线）、以及分钟级数据（1min/5min/15min/30min/60min）。
