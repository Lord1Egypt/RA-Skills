---
name: quant_trading-skills
description: 获取股票/基金等金融标的的量化数据，包括行情数据、财务数据、资金流向数据和舆情数据。支持单只股票查询和批量数据拉取。当用户需要查询股票行情、财务指标、资金流向或相关舆情信息时使用此技能。
version: 1.1.0
author: ""
license: MIT
parameters:
  type: object
  properties:
    type:
      type: string
      description: 数据类型
      enum: [market, finance, fund_flow, public_opinion, stock_codes, batch_market, batch_north_flow, batch_lhb, batch_sentiment, batch_financial]
    symbol:
      type: string
      description: 标的代码，例如 600519（贵州茅台）
    period:
      type: string
      description: 行情周期（仅 market 类型需要）
      enum: [1d, 1w, 1M]
    report_type:
      type: string
      description: 报告类型（仅 finance 类型需要）
      enum: [quarter, year]
    start_date:
      type: string
      description: 开始日期，格式：YYYY-MM-DD
    end_date:
      type: string
      description: 结束日期，格式：YYYY-MM-DD
    stock_codes:
      type: array
      description: 批量拉取时指定的股票代码列表（可选，不指定则拉取全部A股）
      items:
        type: string
    batch_market:
      type: object
      description: 批量行情拉取配置
      properties:
        default_years:
          type: integer
          description: 默认拉取年数
          default: 5
        max_retries:
          type: integer
          description: 最大重试次数
          default: 3
    batch_north_flow:
      type: object
      description: 批量北向资金拉取配置
      properties:
        default_years:
          type: integer
          description: 默认拉取年数
          default: 5
    batch_lhb:
      type: object
      description: 批量龙虎榜拉取配置
      properties:
        default_years:
          type: integer
          description: 默认拉取年数
          default: 3
    batch_sentiment:
      type: object
      description: 批量舆情拉取配置
      properties:
        default_years:
          type: integer
          description: 默认拉取年数
          default: 2
    batch_financial:
      type: object
      description: 批量财报拉取配置
      properties:
        default_years:
          type: integer
          description: 默认拉取年数
          default: 3
        max_retries:
          type: integer
          description: 最大重试次数
          default: 3
  required: [type]
output_format:
  type: object
  schema:
    type: object
    properties:
      success:
        type: boolean
        description: 是否成功
      data:
        type: object
        description: 数据内容
      message:
        type: string
        description: 提示信息
trigger:
  keywords: ["股票", "行情", "财务", "资金流向", "舆情", "股价", "财报", "批量", "北向资金", "龙虎榜"]
  description: 当用户查询股票行情、财务数据、资金流向、舆情信息或需要批量拉取数据时触发
---

# 量化数据获取

## 概述

本 Skill 用于获取股票/基金等金融标的的量化数据，支持以下四类数据：

1. **行情数据 (market)**：获取股票历史行情数据，包括开盘价、收盘价、最高价、最低价、成交量等
2. **财务数据 (finance)**：获取股票财务指标数据，包括营业收入、净利润、ROE、资产负债率等
3. **资金流向数据 (fund_flow)**：获取个股资金流向数据，包括主力净流入、超大单净流入等
4. **舆情数据 (public_opinion)**：获取相关舆情信息

## 使用说明

### 基本调用方式

OpenClaw 通过调用 `index.js` 中导出的 `execute` 函数来使用此 Skill：

```javascript
const { execute } = require('./quant_data_fetch');

const result = await execute(params, context);
```

### 输入参数

| 参数名 | 类型 | 必填 | 说明 | 可选值 |
|--------|------|------|------|--------|
| type | string | 是 | 数据类型 | market, finance, fund_flow, public_opinion |
| symbol | string | 是 | 标的代码 | 例如 600519（贵州茅台） |
| period | string | 否 | 行情周期（仅 market 类型需要） | 1d, 1w, 1M |
| report_type | string | 否 | 报告类型（仅 finance 类型需要） | quarter, year |
| start_date | string | 否 | 开始日期 | 格式：YYYY-MM-DD |
| end_date | string | 否 | 结束日期 | 格式：YYYY-MM-DD |

### 输出格式

```json
{
  "success": true,
  "data": {...},
  "message": "数据获取成功"
}
```

## 数据类型详解

### 1. 行情数据 (market)

获取股票历史行情数据。

**调用示例：**
```javascript
const result = await execute({
  type: 'market',
  symbol: '600519',
  period: '1d',
  start_date: '2024-01-01',
  end_date: '2024-01-31'
});
```

**返回数据示例：**
```json
{
  "success": true,
  "data": {
    "symbol": "600519",
    "period": "1d",
    "items": [
      {
        "date": "2024-01-01",
        "open": 1700.0,
        "high": 1750.0,
        "low": 1690.0,
        "close": 1730.0,
        "volume": 1000000,
        "amount": 1730000000,
        "change": 30.0,
        "change_percent": 1.76,
        "turnover": 0.5
      }
    ]
  },
  "message": "数据获取成功"
}
```

**字段说明：**
- `date`: 日期
- `open`: 开盘价
- `high`: 最高价
- `low`: 最低价
- `close`: 收盘价
- `volume`: 成交量
- `amount`: 成交额
- `change`: 涨跌额
- `change_percent`: 涨跌幅(%)
- `turnover`: 换手率(%)

### 2. 财务数据 (finance)

获取股票财务指标数据。

**调用示例：**
```javascript
const result = await execute({
  type: 'finance',
  symbol: '600519',
  report_type: 'quarter'
});
```

**返回数据示例：**
```json
{
  "success": true,
  "data": {
    "symbol": "600519",
    "report_type": "quarter",
    "items": [
      {
        "report_date": "2023-12-31",
        "revenue": 120000000000,
        "gross_profit": 80000000000,
        "net_profit": 40000000000,
        "eps": 32.0,
        "roe": 25.0,
        "asset_liability_ratio": 30.0,
        "operating_cash_flow": 35000000000
      }
    ]
  },
  "message": "数据获取成功"
}
```

**字段说明：**
- `report_date`: 报告日期
- `revenue`: 营业收入(元)
- `gross_profit`: 营业利润(元)
- `net_profit`: 净利润(元)
- `eps`: 每股收益(元)
- `roe`: 净资产收益率(%)
- `asset_liability_ratio`: 资产负债率(%)
- `operating_cash_flow`: 经营活动产生的现金流量净额(元)

### 3. 资金流向数据 (fund_flow)

获取个股资金流向数据。

**调用示例：**
```javascript
const result = await execute({
  type: 'fund_flow',
  symbol: '600519'
});
```

**返回数据示例：**
```json
{
  "success": true,
  "data": {
    "symbol": "600519",
    "items": [
      {
        "date": "2024-01-01",
        "main_inflow": 50000000,
        "main_inflow_rate": 2.5,
        "超大_inflow": 30000000,
        "超大_inflow_rate": 1.5,
        "large_inflow": 20000000,
        "large_inflow_rate": 1.0,
        "medium_inflow": -5000000,
        "medium_inflow_rate": -0.25,
        "small_inflow": -45000000,
        "small_inflow_rate": -2.25
      }
    ]
  },
  "message": "数据获取成功"
}
```

**字段说明：**
- `date`: 日期
- `main_inflow`: 主力净流入-净额(万元)
- `main_inflow_rate`: 主力净流入-净占比(%)
- `超大_inflow`: 超大单净流入-净额(万元)
- `超大_inflow_rate`: 超大单净流入-净占比(%)
- `large_inflow`: 大单净流入-净额(万元)
- `large_inflow_rate`: 大单净流入-净占比(%)
- `medium_inflow`: 中单净流入-净额(万元)
- `medium_inflow_rate`: 中单净流入-净占比(%)
- `small_inflow`: 小单净流入-净额(万元)
- `small_inflow_rate`: 小单净流入-净占比(%)

### 4. 舆情数据 (public_opinion)

获取相关舆情信息。

**调用示例：**
```javascript
const result = await execute({
  type: 'public_opinion',
  symbol: '600519'
});
```

**返回数据示例：**
```json
{
  "success": true,
  "data": {
    "symbol": "600519",
    "items": [
      {
        "date": "2024-01-01",
        "source": "东方财富网",
        "title": "贵州茅台发布2024年第一季度财报，净利润同比增长20%",
        "sentiment": "positive",
        "url": "https://www.eastmoney.com/600519"
      }
    ]
  },
  "message": "数据获取成功"
}
```

**字段说明：**
- `date`: 日期
- `source`: 来源
- `title`: 标题
- `sentiment`: 情感倾向 (positive/negative/neutral)
- `url`: 链接

## 安装要求

- **Node.js**: >= 16.0.0
- **Python**: >= 3.11.0

## 安装步骤

1. 安装 Node.js 依赖
   ```bash
   npm install
   ```

2. 安装 Python 依赖
   ```bash
   python install.py
   ```
   或
   ```bash
   pip install -r requirements.txt
   ```

## 目录结构

```
quant_trading-skills/
├── SKILL.md              # 技能核心定义文档
├── README.md             # 使用说明
├── package.json          # Node.js 依赖配置
├── requirements.txt      # Python 依赖配置
├── install.py            # 自动安装脚本
├── index.js              # 主入口文件
├── lib/                  # 核心库
│   ├── utils.js          # 工具函数
│   └── dataFetcher.js    # 数据拉取函数
└── scripts/              # 执行脚本
    └── akshare_fetcher.py # Python 数据拉取脚本
```

## 缓存机制

本 Skill 实现了内存缓存机制，相同参数的请求会缓存 1 小时，避免重复请求相同数据。

## 异常处理

Skill 会捕获并处理所有异常，返回统一的错误格式：

```json
{
  "success": false,
  "data": null,
  "message": "执行失败: 错误信息"
}
```

## 批量拉取功能

本 Skill 支持批量拉取各类数据，适用于数据初始化或增量更新场景。

### 批量拉取类型

| 类型 | 说明 | 数据源 |
|------|------|--------|
| batch_market | 批量拉取A股行情数据 | akshare |
| batch_north_flow | 批量拉取北向资金数据 | akshare |
| batch_lhb | 批量拉取龙虎榜数据 | akshare |
| batch_sentiment | 批量拉取舆情数据 | akshare |
| batch_financial | 批量拉取财报数据 | akshare |
| stock_codes | 获取全部A股股票代码列表 | akshare |

### 批量拉取调用示例

#### 1. 批量拉取行情数据

```javascript
const result = await execute({
  type: 'batch_market',
  batch_market: {
    default_years: 5,
    max_retries: 3
  }
});
```

**返回数据示例：**
```json
{
  "success": true,
  "data": {
    "total_stocks": 5000,
    "success_count": 4980,
    "failed_count": 20,
    "total_records": 5000000,
    "is_incremental": false,
    "elapsed_seconds": 1800.5
  },
  "message": "批量拉取完成，成功 4980 只，失败 20 只"
}
```

#### 2. 批量拉取北向资金数据

```javascript
const result = await execute({
  type: 'batch_north_flow',
  batch_north_flow: {
    default_years: 5
  }
});
```

#### 3. 批量拉取龙虎榜数据

```javascript
const result = await execute({
  type: 'batch_lhb',
  batch_lhb: {
    default_years: 3
  }
});
```

#### 4. 批量拉取舆情数据

```javascript
const result = await execute({
  type: 'batch_sentiment',
  batch_sentiment: {
    default_years: 2
  }
});
```

#### 5. 批量拉取财报数据

```javascript
const result = await execute({
  type: 'batch_financial',
  batch_financial: {
    default_years: 3,
    max_retries: 3
  }
});
```

#### 6. 获取股票代码列表

```javascript
const result = await execute({
  type: 'stock_codes'
});
```

**返回数据示例：**
```json
{
  "success": true,
  "data": {
    "items": [
      { "code": "000001", "name": "平安银行" },
      { "code": "000002", "name": "万科A" }
    ],
    "total": 5000
  },
  "message": "数据获取成功"
}
```

## 增量拉取机制

本 Skill 实现了智能增量拉取机制，避免重复拉取已有数据。

### 工作原理

1. **状态记录**：每次批量拉取完成后，会在 `config/fetch_status.json` 中记录拉取时间
2. **日期计算**：下次拉取时，根据上次拉取时间计算需要获取的日期范围
3. **增量标识**：返回结果中 `is_incremental` 字段标识是否为增量拉取

### 状态文件结构

```json
{
  "market": {
    "last_fetch_time": "2024-01-15 10:30:00",
    "fetch_count": 5,
    "last_fetch_count": 4980
  },
  "north_flow": {
    "last_fetch_time": "2024-01-15 11:00:00",
    "fetch_count": 3,
    "last_fetch_count": 1200
  },
  "lhb": {
    "last_fetch_time": "2024-01-15 11:30:00",
    "fetch_count": 2,
    "last_fetch_count": 500
  },
  "sentiment": {
    "last_fetch_time": "2024-01-15 12:00:00",
    "fetch_count": 1,
    "last_fetch_count": 10000
  },
  "financial": {
    "last_fetch_time": "2024-01-15 12:30:00",
    "fetch_count": 1,
    "last_fetch_count": 5000
  }
}
```

### 增量拉取逻辑

- **首次拉取**：`is_incremental: false`，拉取 `default_years` 年的数据
- **增量拉取**：`is_incremental: true`，仅拉取上次拉取时间之后的新数据
- **时间间隔**：从上次拉取时间的下一天开始，到当前日期结束

## Parquet 存储格式

所有批量拉取的数据均采用 **Apache Parquet** 格式存储，具有以下优势：

### 存储优势

- **高效压缩**：使用 Snappy 压缩算法，压缩率高
- **列式存储**：支持列级别的数据读取，查询效率高
- **跨平台兼容**：支持 Python、Java、JavaScript 等多种语言读取
- **Schema 演进**：支持 Schema 变更，便于数据结构升级

### 技术规格

| 属性 | 值 |
|------|-----|
| 压缩算法 | Snappy |
| 文件格式 | Apache Parquet |
| 依赖库 | pyarrow >= 14.0.0 |

## 数据分区存储结构

批量拉取的数据按照不同维度进行分区存储，便于数据管理和查询。

### 目录结构

```
data/
├── market/                    # 行情数据
│   ├── 000001/               # 股票代码
│   │   ├── 2024-01.parquet   # 按月分区
│   │   ├── 2024-02.parquet
│   │   └── ...
│   ├── 000002/
│   └── ...
├── north_flow/               # 北向资金数据
│   ├── 2024-01.parquet      # 按月分区
│   ├── 2024-02.parquet
│   └── ...
├── lhb/                      # 龙虎榜数据
│   ├── 2024-01-15.parquet   # 按日分区
│   ├── 2024-01-16.parquet
│   └── ...
├── sentiment/                # 舆情数据
│   ├── 000001/              # 股票代码
│   │   ├── 2024-01-15.parquet  # 按日分区
│   │   └── ...
│   └── ...
└── financial/                # 财报数据
    ├── 000001/              # 股票代码
    │   ├── 2024.parquet     # 按年分区
    │   ├── 2023.parquet
    │   └── ...
    └── ...
```

### 分区策略

| 数据类型 | 分区维度 | 文件命名规则 | 说明 |
|----------|----------|--------------|------|
| market | 股票代码 + 月份 | `{symbol}/{YYYY-MM}.parquet` | 按股票代码和月份分区 |
| north_flow | 月份 | `{YYYY-MM}.parquet` | 按月份分区 |
| lhb | 日期 | `{YYYY-MM-DD}.parquet` | 按日期分区 |
| sentiment | 股票代码 + 日期 | `{symbol}/{YYYY-MM-DD}.parquet` | 按股票代码和日期分区 |
| financial | 股票代码 + 年份 | `{symbol}/{YYYY}.parquet` | 按股票代码和年份分区 |

### 数据去重策略

在增量拉取时，系统会自动处理重复数据：

1. **读取现有数据**：读取已存在的 Parquet 文件
2. **合并新数据**：将新数据与现有数据合并
3. **去重处理**：根据主键字段去重，保留最新数据
4. **覆盖写入**：将合并后的数据写回文件

### 主键字段

| 数据类型 | 主键字段 |
|----------|----------|
| market | date |
| north_flow | date |
| lhb | date, symbol |
| sentiment | date, title |
| financial | report_date |

## 注意事项

1. 确保 Python 版本 >= 3.11
2. 确保已正确安装所有 Python 依赖（akshare、pandas、pyarrow）
3. 网络连接正常，以便 akshare 获取实时数据
4. 股票代码格式：上海市场以 6 开头，深圳市场以 0 或 3 开头
5. 批量拉取耗时较长，建议在非交易时间执行
6. 首次批量拉取会获取历史数据，耗时可能超过 1 小时
7. 增量拉取仅获取新数据，耗时较短
