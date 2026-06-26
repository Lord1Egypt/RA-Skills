# 股票API参考文档

## 免费股票数据API

### 1. 东方财富 (East Money) - 推荐用于A股/港股

**基础URL**: `https://push2.eastmoney.com/`

**实时行情接口**:
```
GET /api/qt/stock/get?secid=市场.代码&fields=字段列表
```

**市场代码**:
- `0` - 上海证券交易所 (沪股通)
- `1` - 深圳证券交易所 (深股通)
- `0.6` - 上海主板
- `0.3` - 创业板
- `0.9` - 科创板

**字段说明**:
| 字段 | 说明 |
|------|------|
| f43 | 最新价 |
| f44 | 涨跌 |
| f45 | 涨跌幅 |
| f46 | 成交量 |
| f47 | 成交额 |
| f48 | 振幅 |
| f50 | 股票代码 |
| f57 | 股票名称 |
| f58 | 市场 |

**示例**:
```bash
# 贵州茅台 (600519)
curl "https://push2.eastmoney.com/api/qt/stock/get?secid=1.600519&fields=f43,f44,f45,f57,f58"

# 腾讯控股 (00700)
curl "https://push2.eastmoney.com/api/qt/stock/get?secid=0.700&fields=f43,f44,f45,f57,f58"
```

### 2. Yahoo Finance - 推荐用于美股

**基础URL**: `https://query1.finance.yahoo.com/v8/finance/chart/`

**实时行情接口**:
```
GET /v8/finance/chart/{symbol}?interval=1d&range=1d
```

**示例**:
```bash
# Apple
curl "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=1d"

# Microsoft
curl "https://query1.finance.yahoo.com/v8/finance/chart/MSFT?interval=1d&range=1d"
```

### 3. Alpha Vantage - 美股/外汇

**基础URL**: `https://www.alphavantage.co/query`

**获取API Key**: https://www.alphavantage.co/support/#api-key

**示例**:
```bash
curl "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_API_KEY"
```

### 4. iTick - 综合股票数据

**文档**: https://docs.itick.org/

**特点**:
- 支持A股、港股、美股
- 提供REST和WebSocket接口
- 需要注册获取Token

---

## 股票代码格式

### A股
| 市场 | 代码示例 | 说明 |
|------|----------|------|
| 上海主板 | 600519 | 6开头 |
| 上海科创板 | 688111 | 688开头 |
| 深圳主板 | 000001 | 0开头 |
| 创业板 | 300001 | 3开头 |

### 港股
| 市场 | 代码示例 | 说明 |
|------|----------|------|
| 主板 | 00700 | 5位数字 |
| 创业板 | 8001 | 8位数字 |

### 美股
| 市场 | 代码示例 | 说明 |
|------|----------|------|
| 纳斯达克 | AAPL, GOOGL | 字母代码 |
| 纽交所 | MSFT, JPM | 字母代码 |

---

## 数据字段说明

### 股票基本信息
```json
{
  "code": "00700",
  "name": "腾讯控股",
  "price": 395.00,
  "change": 10.00,
  "change_percent": 2.60,
  "volume": 15000000,
  "amount": 5850000000,
  "amplitude": 3.15,
  "high": 398.00,
  "low": 385.00,
  "open": 386.00,
  "close": 385.00,
  "market_cap": 3700000000000,
  "pe_ratio": 25.5,
  "dividend_yield": 0.35
}
```

---

## 汇率参考

| 货币 | 汇率(约) | 更新时间 |
|------|----------|----------|
| 美元 (USD) | 7.20 | 实时 |
| 港币 (HKD) | 0.92 | 实时 |

---

## 使用注意事项

1. **数据延迟**: 免费API通常有15分钟延迟
2. **调用频率**: 注意API的调用频率限制
3. **备用方案**: 准备模拟数据作为降级方案
4. **投资风险**: 所有数据仅供参考，不构成投资建议
