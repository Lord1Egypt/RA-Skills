# Open API · 行情（快照、分时、K 线）

> 根地址、`API_BASE`、统一响应与鉴权见 [api.md](./api.md)。

### 12. 单合约行情快照

```
GET /open/v1/market/snapshot?instrumentId=au2606
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live

Query（二选一，优先 instrumentId）：
  instrumentId   合约代码，如 au2606
  contractCode   合约代码别名（兼容旧调用）
```

**响应 `data`：**

```json
{
  "instrumentId": "au2606",
  "exchangeId": "SHFE",
  "instrumentName": "沪金2606",
  "volumeMultiple": 1000,
  "priceTick": "0.02",
  "lastPrice": "790.50",
  "openPrice": "789.80",
  "highestPrice": "792.00",
  "lowestPrice": "788.60",
  "bidPrice1": "790.48",
  "bidVolume1": "3",
  "askPrice1": "790.50",
  "askVolume1": "5",
  "preSettlementPrice": "788.00",
  "settlementPrice": "790.20",
  "tradingDay": "20260327",
  "updateTime": "2026-03-27 10:15:30"
}
```

> 该接口只读 Redis 缓存，不回源 DB/CTP；缓存缺失时字段可能为 `null`。

---

### 13. 批量行情快照

```
GET /open/v1/market/snapshots?instrumentIds=au2606,ag2612,cu2506
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

`instrumentIds`：逗号分隔，如 `au2606,ag2612,cu2506`，最多建议 20 个。

响应 `data` 为数组，每个元素结构与单合约快照完全相同（见第 12 节）。数组顺序与请求中 `instrumentIds` 顺序一致。

---

### 14. 分时图

```
GET /open/v1/market/tick?exchangeId=SHFE&instrumentId=au2606
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

| Query 参数 | 必填 | 说明 |
|-----------|------|------|
| `exchangeId` | **是** | 交易所代码，如 `SHFE`、`DCE`、`CZCE`、`INE`、`CFFEX` |
| `instrumentId` | **是** | 合约代码，如 `au2606` |

**响应 `data`：**

```json
{
  "startTime": "09:00:00",
  "endTime": "15:00:00",
  "closeTime": "15:00:00",
  "totalVolume": "58000",
  "reqTime": 1743040800,
  "ticks": [
    { "t": "1743040800", "p": "790.50", "v": "120", "i": "121000", "a": "94860" },
    { "t": "1743040860", "p": "790.80", "v": "85",  "i": "121050", "a": "67218" }
  ]
}
```

**`ticks` 数组每条字段（字段名均为单字母）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `t` | string | 时间戳（秒） |
| `p` | string | 价格 |
| `v` | string | 该分钟成交量 |
| `i` | string | 持仓量 |
| `a` | string | 成交额（价格×量，取整） |

| 外层字段 | 类型 | 说明 |
|---------|------|------|
| `startTime` | string | 交易开始时间，如 `09:00:00` |
| `endTime` | string | 交易结束时间，如 `15:00:00` |
| `closeTime` | string | 收盘时间 |
| `totalVolume` | string | 全日总成交量 |
| `reqTime` | number | 请求时间戳（秒） |

---

### 15. K 线图

```
GET /open/v1/market/kline?exchangeId=SHFE&instrumentId=au2606&type=6
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

| Query 参数 | 必填 | 说明 |
|-----------|------|------|
| `exchangeId` | **是** | 交易所代码 |
| `instrumentId` | **是** | 合约代码 |
| `type` | **是** | K 线周期（见下表） |

**K 线周期 `type` 枚举：**

| type 值 | 说明 |
|---------|------|
| `10` | 1 分钟 |
| `2` | 5 分钟 |
| `3` | 15 分钟 |
| `4` | 30 分钟 |
| `9` | 4 小时 |
| `5` | 1 小时 |
| `6` | 日线 |
| `7` | 周线 |

**响应 `data`：**

```json
{
  "totalVolume": "320000",
  "reqTime": 1743040800,
  "chats": [
    {
      "t": "2026-03-20",
      "o": "788.00",
      "h": "795.00",
      "l": "786.50",
      "c": "792.00",
      "v": "45000",
      "a": "35640000",
      "u": 1742428800,
      "i": "118000",
      "s": "791.50"
    },
    {
      "t": "2026-03-21",
      "o": "792.00",
      "h": "798.00",
      "l": "790.00",
      "c": "796.00",
      "v": "52000",
      "a": "41392000",
      "u": 1742515200,
      "i": "120000",
      "s": "795.00"
    }
  ]
}
```

**`chats` 数组每条字段（字段名均为单字母）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `t` | string | 时间标签（分钟线格式 `MM-dd HH:mm`；日线格式 `yyyy-MM-dd`） |
| `o` | string | 开盘价 |
| `h` | string | 最高价 |
| `l` | string | 最低价 |
| `c` | string | 收盘价 |
| `v` | string | 成交量 |
| `a` | string | 成交额（取整） |
| `u` | number | 时间戳（秒） |
| `i` | string | 持仓量 |
| `s` | string | 结算价（**仅日K线有值**，其他周期为 `null`/`"0"`） |

| 外层字段 | 类型 | 说明 |
|---------|------|------|
| `totalVolume` | string | 最新一根 K 线对应的全日总成交量 |
| `reqTime` | number | 请求时间戳（秒） |

---
