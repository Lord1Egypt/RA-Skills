# Open API · 品种与合约目录

> 根地址、`API_BASE`、统一响应与鉴权见 [api.md](./api.md)。

### 16. 品种 + 主力合约分页

```
GET /open/v1/catalog/goods
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

| Query 参数 | 类型 | 默认 | 说明 |
|-----------|------|------|------|
| `excode` | string | 无 | 交易所代码；传 `__NIGHT__` 筛选有夜盘品种 |
| `page` | int | `1` | 页码 |
| `pageSize` | int | `20` | 每页条数，最大 100 |
| `sortType` | int | 无 | `1` 涨幅 / `2` 跌幅 / `3` 成交量 / `4` 增仓 |
| `category` | string | 无 | 商品分类 |
| `productId` | string | 无 | 品种代码；与 `excode` 同传时返回该品种下所有合约 |
| `onlyMainInCategory` | boolean | 无 | 与 `category` 联用：仅该分类主力合约 |
| `allContractsByExcode` | boolean | 无 | 与 `excode` 联用：该所全部有效合约（非仅主力） |

**响应 `data`：**

```json
{
  "total": 86,
  "page": 1,
  "pageSize": 20,
  "list": [
    {
      "excode": "SHFE",
      "goodsCode": "au",
      "goodsName": "黄金",
      "productId": "au",
      "tradeTime": "21:00-02:30,09:00-11:30,13:30-15:00",
      "startTime": "21:00",
      "middleTime": "02:30",
      "endTime": "15:00",
      "nextDayFlag": 1,
      "mainContractCode": "au2606",
      "isPrincipal": 1,
      "mainContractQuotation": {
        "instrumentID": "au2606",
        "exchangeID": "SHFE",
        "lastPrice": "790.50",
        "change": "2.50",
        "chg": "0.32",
        "volume": "58000",
        "openInterest": "121000",
        "upperLimitPrice": "830.00",
        "lowerLimitPrice": "750.00"
      }
    }
  ]
}
```

**字段提示：**
- `nextDayFlag`：**`1` = 该品种支持夜盘**，`0` = 无夜盘。
- `isPrincipal`：**`1` = 当前主力合约**（随换月变化）。
- `mainContractQuotation` 行情数据字段均为 string 类型（含价格、量等），需要计算时须 parseFloat。

---

### 17. 品种详情

```
GET /open/v1/catalog/goods/detail?excode=SHFE&code=au
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

| Query 参数 | 必填 | 说明 |
|-----------|------|------|
| `excode` | **是** | 交易所代码，如 `SHFE` |
| `code` | **是** | 商品代码（品种），如 `au`、`cu`、`ag` |

**响应 `data`：**

```json
{
  "goods": {
    "excode": "SHFE",
    "goodsCode": "au",
    "goodsName": "黄金",
    "productId": "au",
    "tradeTime": "21:00-02:30,09:00-11:30,13:30-15:00",
    "nextDayFlag": 1,
    "category": "贵金属"
  },
  "calendarNightSessionTonight": true
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `goods.nextDayFlag` | int | **`1` = 该品种支持夜盘**，`0` = 无夜盘 |
| `goods.tradeTime` | string | 完整交易时段描述 |
| `calendarNightSessionTonight` | boolean | 交易日历层面今晚是否有夜盘（与 `nextDayFlag` 是独立维度） |

---

### 18. 合约详情

```
GET /open/v1/catalog/contract?contractCode=au2606
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

含是否主力（`isPrincipal`）、乘数（`volumeMultiple`）、交易时间、保证金率等。

**响应 `data`：**

```json
{
  "excode": "SHFE",
  "exname": "上海期货交易所",
  "contractCode": "au2606",
  "productId": "au",
  "goodsName": "黄金",
  "isPrincipal": 1,
  "volumeMultiple": 1000,
  "priceTick": 0.02,
  "priceLimit": 5.00,
  "shortMarginRatioByMoney": 0.05,
  "tradeTime": "21:00-02:30,09:00-11:30,13:30-15:00",
  "startTime": "21:00",
  "middleTime": "02:30",
  "endTime": "15:00",
  "nextDayFlag": 1,
  "openDate": "2024-01-15",
  "expireDate": "2026-06-27",
  "startDeliveryDate": "2026-06-01",
  "endDeliveryDate": "2026-06-27",
  "deliveryMonth": "2026-06",
  "deliveryGrade": "符合GB/T 4134-2003 Au99.99标准",
  "eastmoneyDetail": null
}
```

**关键字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `isPrincipal` | int | `1` = 当前主力，`0` = 非主力 |
| `volumeMultiple` | int | 合约乘数（计算盈亏必须用此值） |
| `priceTick` | number | 最小变动单位（报价精度） |
| `priceLimit` | number | 涨跌停幅度百分比（**仅供参考**） |
| `shortMarginRatioByMoney` | number | 保证金率（**仅供参考**，实际以期货公司为准） |
| `nextDayFlag` | int | `1` = 有夜盘（跨自然日），`0` = 无夜盘 |
| `expireDate` | string | 合约到期日 |

> `priceLimit`、`shortMarginRatioByMoney` 等保证金与涨跌停字段**仅供参考**，以交易所和期货公司实际为准。

---

### 19. 合约 F10

```
GET /open/v1/catalog/contract/f10?contractCode=au2606
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

返回东财商品详情 + 摘要字段（含长文本）。

**响应 `data`：**

```json
{
  "contractCode": "au2606",
  "excode": "SHFE",
  "productId": "au",
  "goodsName": "黄金",
  "isPrincipal": 1,
  "tradeTime": "21:00-02:30,09:00-11:30,13:30-15:00",
  "shortMarginRatioByMoney": 0.05,
  "priceLimitPercent": 5.00,
  "disclaimer": "实际交易保证金与费率以交易所及期货公司结算为准；本数据仅供参考",
  "eastmoneyDetail": {
    "deliveryUnit": "1000克/手",
    "tradingUnit": "1手=1000克",
    "quotationUnit": "元/克",
    "minPriceChange": "0.02元/克",
    "deliveryGrade": "符合GB/T 4134-2003 Au99.99标准",
    "deliveryPlace": "交易所指定仓库",
    "lastTradingDay": "合约到期月份的第五个交易日",
    "margin": "合约价值的5%"
  }
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `priceLimitPercent` | number | 涨跌停幅度百分比（仅供参考） |
| `eastmoneyDetail` | object \| null | 东财 F10 扩展信息；未收录的合约为 `null` |
| `disclaimer` | string | 数据免责声明 |

---

### 20. 热门合约 TOP10

```
GET /open/v1/catalog/hot
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

近 30 分钟成交量排名前 10 的合约。

**响应 `data`（数组，结构与合约详情相同）：**

```json
[
  {
    "excode": "SHFE",
    "contractCode": "au2606",
    "productId": "au",
    "goodsName": "黄金",
    "isPrincipal": 1,
    "volumeMultiple": 1000,
    "priceTick": 0.02,
    "tradeTime": "21:00-02:30,09:00-11:30,13:30-15:00",
    "nextDayFlag": 1,
    "expireDate": "2026-06-27"
  },
  {
    "excode": "DCE",
    "contractCode": "m2509",
    "productId": "m",
    "goodsName": "豆粕",
    "isPrincipal": 1,
    "volumeMultiple": 10,
    "priceTick": 1.0,
    "tradeTime": "21:00-23:30,09:00-11:30,13:30-15:00",
    "nextDayFlag": 1,
    "expireDate": "2025-09-14"
  }
]
```

---

### 21. 交易所列表

```
GET /open/v1/catalog/exchanges
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

按商品数量降序。

**响应 `data`：**

```json
[
  { "excode": "SHFE", "count": 32 },
  { "excode": "DCE",  "count": 28 },
  { "excode": "CZCE", "count": 25 },
  { "excode": "CFFEX","count": 6  },
  { "excode": "INE",  "count": 4  },
  { "excode": "GFEX", "count": 3  }
]
```

---

### 22. 当晚是否有夜盘

```
GET /open/v1/catalog/session/night-today
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

**响应 `data`：**

```json
{
  "hasNightSessionTonight": true,
  "date": "2026-03-27"
}
```

> `hasNightSessionTonight` 表示**交易日历**层面今晚是否排有夜盘，与某品种 `deleteFlag` 是否支持夜盘是**独立维度**。

---
