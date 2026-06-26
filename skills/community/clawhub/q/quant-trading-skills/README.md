# quant\_trading-skills Skill

## 简介

quant\_trading-skills 是一个符合 OpenClaw 官方规范的 Skill，用于获取股票/基金等金融标的的量化数据，包括行情、财务、资金流向和舆情数据。支持单只股票查询和批量数据拉取。

## 功能特性

- **单只股票查询**：获取指定股票的行情、财务、资金流向、舆情数据
- **批量数据拉取**：支持批量拉取全部A股的行情、北向资金、龙虎榜、舆情、财报数据
- **增量更新**：智能增量拉取机制，避免重复拉取已有数据
- **Parquet 存储**：采用高效的列式存储格式，支持压缩和快速查询
- **分区存储**：按时间维度分区存储，便于数据管理和查询

## 目录结构

```
quant_trading-skills/
  ├── index.js              # 主入口文件
  ├── package.json          # Node.js 依赖配置
  ├── requirements.txt      # Python 依赖配置
  ├── README.md             # 使用说明
  ├── SKILL.md              # Skill 定义文档
  ├── install.py            # 自动安装脚本
  ├── config/               # 配置文件
  │   ├── fetch_status.json # 拉取状态记录
  │   └── data_config.json  # 数据配置
  ├── data/                 # 数据存储目录
  │   ├── market/           # 行情数据（按股票代码/月份分区）
  │   ├── north_flow/       # 北向资金数据（按月份分区）
  │   ├── lhb/              # 龙虎榜数据（按日期分区）
  │   ├── sentiment/        # 舆情数据（按股票代码/日期分区）
  │   └── financial/        # 财报数据（按股票代码/年份分区）
  ├── lib/                  # 工具函数
  │   ├── utils.js          # 工具函数（缓存、日志、参数校验等）
  │   └── dataFetcher.js    # 数据拉取函数
  ├── test/                 # 测试文件
  │   ├── test.js           # 基本功能测试
  │   ├── test_batch.js     # 批量拉取功能测试
  │   └── test_lhb.py       # 龙虎榜数据测试
  └── scripts/              # 执行脚本
      ├── akshare_fetcher.py # Python 数据拉取脚本（基于 akshare）
      ├── data_storage.py   # 数据存储模块（Parquet 格式）
      └── fetch_status.py   # 拉取状态管理模块
```

## 环境要求

- Node.js: >=16.0.0
- Python: >=3.11.0

## 安装依赖

### Node.js 依赖

```bash
cd quant_data_fetch
npm install
```

### Python 依赖

```bash
cd quant_data_fetch
pip install -r requirements.txt
```

**依赖列表：**

- akshare >= 1.18.0（数据源）
- pandas >= 2.0.0（数据处理）
- pyarrow >= 14.0.0（Parquet 存储格式）

## 使用方法

作为 OpenClaw Skill 使用，调用 `execute` 方法：

```javascript
const { execute } = require('./quant_trading-skills');

async function main() {
  const result = await execute({
    type: 'market',      // 数据类型：market, finance, fund_flow, public_opinion
    symbol: '600519',    // 标的代码
    period: '1d',        // 行情周期（仅market类型需要）
    start_date: '2024-01-01', // 开始日期（可选）
    end_date: '2024-01-31'     // 结束日期（可选）
  });
  
  console.log(result);
}

main();
```

## 参数说明

### 单只股票查询参数

| 参数           | 类型     | 必需  | 说明                  | 示例                                                         |
| ------------ | ------ | --- | ------------------- | ---------------------------------------------------------- |
| type         | string | 是   | 数据类型                | market, finance, fund\_flow, public\_opinion, stock\_codes |
| symbol       | string | 是\* | 标的代码                | 600519（贵州茅台）                                               |
| period       | string | 否   | 行情周期（仅market类型需要）   | 1m, 5m, 15m, 30m, 60m, 1d, 1w, 1M                          |
| report\_type | string | 否   | 报告类型（仅finance类型需要）  | quarter, year                                              |
| start\_date  | string | 否   | 开始日期（格式：YYYY-MM-DD） | 2024-01-01                                                 |
| end\_date    | string | 否   | 结束日期（格式：YYYY-MM-DD） | 2024-01-31                                                 |

\*注：单只股票查询时 symbol 为必需参数，批量拉取时不需要

### 批量拉取参数

| 参数                 | 类型     | 必需 | 说明       | 示例                                                                                |
| ------------------ | ------ | -- | -------- | --------------------------------------------------------------------------------- |
| type               | string | 是  | 批量拉取类型   | batch\_market, batch\_north\_flow, batch\_lhb, batch\_sentiment, batch\_financial |
| batch\_market      | object | 否  | 行情拉取配置   | { default\_years: 5, max\_retries: 3 }                                            |
| batch\_north\_flow | object | 否  | 北向资金拉取配置 | { default\_years: 5 }                                                             |
| batch\_lhb         | object | 否  | 龙虎榜拉取配置  | { default\_years: 3 }                                                             |
| batch\_sentiment   | object | 否  | 舆情拉取配置   | { default\_years: 2 }                                                             |
| batch\_financial   | object | 否  | 财报拉取配置   | { default\_years: 3, max\_retries: 3 }                                            |

## 返回数据格式

```javascript
{
  "success": true,  // 是否成功
  "data": {...},   // 数据内容
  "message": "数据获取成功"  // 提示信息
}
```

### 行情数据 (market)

```javascript
{
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
}
```

### 财务数据 (finance)

```javascript
{
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
}
```

### 资金流向数据 (fund\_flow)

```javascript
{
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
}
```

### 舆情数据 (public\_opinion)

```javascript
{
  "symbol": "600519",
  "items": [
    {
      "date": "2024-01-01",
      "source": "东方财富网",
      "title": "贵州茅台发布2023年年度报告，净利润同比增长15%",
      "sentiment": "positive",
      "url": "https://www.eastmoney.com/600519"
    }
  ]
}
```

## 示例

### 获取行情数据

```javascript
const result = await execute({
  type: 'market',
  symbol: '600519',
  period: '1d',
  start_date: '2024-01-01',
  end_date: '2024-01-31'
});
```

### 获取财务数据

```javascript
const result = await execute({
  type: 'finance',
  symbol: '600519',
  report_type: 'quarter'
});
```

### 获取资金流向数据

```javascript
const result = await execute({
  type: 'fund_flow',
  symbol: '600519'
});
```

### 获取舆情数据

```javascript
const result = await execute({
  type: 'public_opinion',
  symbol: '600519'
});
```

### 获取股票代码列表

```javascript
const result = await execute({
  type: 'stock_codes'
});
```

### 批量拉取行情数据

```javascript
const result = await execute({
  type: 'batch_market',
  batch_market: {
    default_years: 5,
    max_retries: 3
  }
});
```

### 批量拉取北向资金数据

```javascript
const result = await execute({
  type: 'batch_north_flow',
  batch_north_flow: {
    default_years: 5
  }
});
```

### 批量拉取龙虎榜数据

```javascript
const result = await execute({
  type: 'batch_lhb'
});
```

### 批量拉取舆情数据

```javascript
const result = await execute({
  type: 'batch_sentiment',
  batch_sentiment: {
    default_years: 2
  }
});
```

### 批量拉取财报数据

```javascript
const result = await execute({
  type: 'batch_financial',
  batch_financial: {
    default_years: 3,
    max_retries: 3
  }
});
```

## 缓存机制

本 Skill 实现了简单的内存缓存机制，缓存时间为 1 小时，避免重复请求相同数据。

## 异常处理

Skill 会捕获并处理所有异常，返回统一的错误格式：

```javascript
{
  "success": false,
  "data": null,
  "message": "执行失败: 错误信息"
}
```

## 日志记录

Skill 会记录详细的日志信息，包括执行开始、参数校验、缓存检查、数据获取、缓存设置和执行结果等。
