# API 参考文档

本文档提供盘前简报 Skill 使用的 API 详细说明。

## 市场温度 API

**端点**：`/market/temp`

**方法**：GET

**认证**：需要 Token

**返回格式**：JSON

```json
{
  "date": "2024-01-15",
  "pe": 35.2,
  "fear_greed": 28.5,
  "trend": 42.3,
  "momentum": 38.7
}
```

**字段说明**：

| 字段       | 类型   | 说明                         |
| ---------- | ------ | ---------------------------- |
| date       | string | 数据日期 (YYYY-MM-DD)        |
| pe         | number | 估值温度 (0-100)             |
| fear_greed | number | 恐贪指数 (0-100)             |
| trend      | number | 趋势温度 (0-100)             |
| momentum   | number | 动量温度 (0-100)             |

---

## 板块热力图 API

**端点**：`/sector/heatmap`

**方法**：GET

**认证**：需要 Token

**返回格式**：JSON

```json
[
  {
    "name": "通信设备",
    "qd": 85.3,
    "zdf": 2.5,
    "zdf5": 5.2,
    "zdf10": 8.7,
    "zdf20": 12.3
  }
]
```

**字段说明**：

| 字段  | 类型   | 说明                  |
| ----- | ------ | --------------------- |
| name  | string | 板块名称              |
| qd    | number | 板块强度 (0-100)      |
| zdf   | number | 当日涨跌幅 (%)        |
| zdf5  | number | 5日涨跌幅 (%)         |
| zdf10 | number | 10日涨跌幅 (%)        |
| zdf20 | number | 20日涨跌幅 (%)        |

---

## 涨跌停 API

**端点**：`/price-limit`

**方法**：GET

**认证**：需要 Token

**返回格式**：JSON

```json
{
  "date": "2024-01-15",
  "up_count": 45,
  "down_count": 12,
  "up_2b_count": 8,
  "up_3b_count": 3,
  "up_ab_count": 15
}
```

**字段说明**：

| 字段        | 类型   | 说明           |
| ----------- | ------ | -------------- |
| date        | string | 数据日期       |
| up_count    | number | 涨停数量       |
| down_count  | number | 跌停数量       |
| up_2b_count | number | 2连板数量      |
| up_3b_count | number | 3连板数量      |
| up_ab_count | number | 涨停开板数量   |

---

## 市场指数 API

**端点**：`/market/index`

**方法**：GET

**认证**：需要 Token

**返回格式**：JSON

```json
{
  "date": "2024-01-15",
  "north_net": 85.2,
  "north_sh": 42.5,
  "north_sz": 42.7,
  "up_count": 2534,
  "down_count": 1823,
  "limit_up": 45,
  "limit_down": 12
}
```

**字段说明**：

| 字段       | 类型   | 说明             |
| ---------- | ------ | ---------------- |
| date       | string | 数据日期         |
| north_net  | number | 北向净流入(亿元) |
| north_sh   | number | 沪股通净流入     |
| north_sz   | number | 深股通净流入     |
| up_count   | number | 上涨家数         |
| down_count | number | 下跌家数         |
| limit_up   | number | 涨停数           |
| limit_down | number | 跌停数           |

---

## 错误码

| 错误码 | 说明               | 处理方式           |
| ------ | ------------------ | ------------------ |
| 401    | 认证失败           | 检查 Token 配置    |
| 404    | API 不存在         | 检查 URL           |
| 429    | 请求频率超限       | 等待后重试         |
| 500    | 服务器内部错误     | 稍后重试           |

---

## 认证

所有 API 请求需要在 Header 中携带 Token：

```
Authorization: Bearer YOUR_TOKEN
```

或通过环境变量：

```bash
export DAXIAPI_TOKEN=YOUR_TOKEN
```

---

## 速率限制

- 每分钟最多 60 次请求
- 建议间隔 1 秒以上
- 超限返回 429 错误

---

## 数据更新时间

| 数据类型   | 更新时间               |
| ---------- | ---------------------- |
| 市场温度   | 交易日晚 8 点后        |
| 板块热力图 | 交易日收盘后           |
| 涨跌停     | 交易日收盘后           |
| 北向资金   | 交易日收盘后           |

---

## 最佳实践

1. **缓存数据**：避免重复请求相同数据
2. **错误重试**：429 错误后等待重试
3. **时效检查**：检查数据日期是否为最新
4. **批量请求**：合并多个 API 调用减少请求数
