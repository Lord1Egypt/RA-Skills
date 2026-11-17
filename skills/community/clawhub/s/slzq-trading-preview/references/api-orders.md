# Open API · 委托、成交、下单与撤单

> 根地址、`API_BASE`、统一响应与鉴权见 [api.md](./api.md)。

### 7. 当前委托

```
GET /open/v1/orders/open
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

近 3 日未完结委托（已报、部分成交等）。响应 `data` 为 `RtnOrderModel` 数组，关键字段见「委托回报字段说明」一节。

**响应 `data` 示例：**

```json
[
  {
    "instrumentId": "cu2506",
    "exchangeId": "SHFE",
    "orderRef": "1001",
    "orderSysId": "31574",
    "frontID": 1,
    "sessionId": 123456,
    "direction": "BUY",
    "offsetFlag": "OPEN",
    "limitPrice": 78500.0,
    "volume": 1,
    "volumeTraded": 0,
    "volumeTotal": 1,
    "orderStatus": "SUBMITTED",
    "statusMsg": "已报",
    "insertDate": "20260327",
    "insertTime": "10:15:30",
    "tradingDay": "20260327"
  }
]
```

---

### 8. 成交列表

```
GET /open/v1/trades
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live

Query 参数（均可选）：
  instrumentId    合约代码，如 cu2506
  exchangeId      交易所代码，如 SHFE
  insertTimeStart 开始时间，格式 yyyy-MM-dd HH:mm:ss，如 2026-03-27 09:00:00
  insertTimeEnd   结束时间，格式 yyyy-MM-dd HH:mm:ss，如 2026-03-27 15:30:00
```

> 不传时间时，**live** 默认返回近 3 日成交；**sim** 返回全部历史。

**响应 `data`（数组）示例：**

```json
[
  {
    "instrumentId": "cu2506",
    "exchangeId": "SHFE",
    "tradeId": "00001",
    "orderRef": "1001",
    "orderSysId": "31574",
    "direction": "BUY",
    "offsetFlag": "OPEN",
    "price": 78500.0,
    "volume": 1,
    "tradeDate": "20260327",
    "tradeTime": "10:15:32",
    "tradingDay": "20260327",
    "profit": null
  }
]
```

**成交回报关键字段（`RtnTradeModel`）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `instrumentId` | string | 合约代码 |
| `exchangeId` | string | 交易所代码 |
| `tradeId` | string | 成交编号（交易所分配） |
| `orderRef` | string | 对应委托的报单引用 |
| `orderSysId` | string | 对应委托的报单编号 |
| `direction` | string | `BUY` / `SELL` |
| `offsetFlag` | string | `OPEN` / `CLOSE` / `CLOSE_TODAY` / `CLOSE_YESTERDAY` |
| `price` | number | 成交价格 |
| `volume` | int | 成交手数 |
| `tradeDate` | string | 成交日期，如 `20260327` |
| `tradeTime` | string | 成交时间，如 `10:15:32` |
| `tradingDay` | string | 交易日 |
| `profit` | number \| null | 平仓成交时柜台返回的实际盈亏（元）；开仓时为 `null` |

---

### 9. 下单

```
POST /open/v1/orders
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
         Content-Type: application/json
```

#### 请求体（JSON）

```json
{
  "instrumentId": "cu2506",
  "orderRef": "1001",
  "direction": "BUY",
  "offsetFlag": "OPEN",
  "priceType": "LIMIT",
  "limitPrice": 78500.0,
  "count": 1,
  "positionDateType": null,
  "timeCondition": "GFD"
}
```

#### 字段说明

| 字段 | 类型 | 必填 | 枚举值 / 格式 | 说明 |
|------|------|------|--------------|------|
| `instrumentId` | string | **是** | 如 `cu2506`、`au2606` | 合约代码，大小写敏感 |
| `orderRef` | string | sim 必填 / live 可省 | 1～13 位纯数字字符串 | **模拟盘**：必填且本次请求内须唯一；**实盘 live**：传入会被忽略，服务端自动生成，撤单时从回报的 `orderRef` 取值 |
| `direction` | string | **是** | `BUY` \| `SELL` | 买入 / 卖出 |
| `offsetFlag` | string | **是** | `OPEN` \| `CLOSE` \| `CLOSE_TODAY` \| `CLOSE_YESTERDAY` | 开仓 / 平仓 / 平今 / 平昨；live 平仓推荐用 `CLOSE`，服务端自动处理 SHFE/INE 拆单 |
| `priceType` | string | **是** | `LIMIT` \| `ANY` \| `BEST` \| `LAST` | 限价 / 市价（任意价）/ 最优价 / 最新价 |
| `limitPrice` | number | **是** | 浮点数，如 `78500.0` | 必须符合合约 priceTick 精度；市价单也需传一个合理价格（服务端以此为参考） |
| `count` | int | **是** | 正整数，如 `1` | 手数，不得超过当前可用持仓（平仓时） |
| `positionDateType` | string | 否 | `"今"` \| `"昨"` \| `null` | 仅 SHFE/INE 区分今昨仓时有效；不传由服务端按策略自动选择 |
| `timeCondition` | string | 否 | `"GFD"` \| `"GTC"` | 有效期：当日有效（默认）/ 撤销前有效 |

#### 实盘 live 平仓行为说明

- 服务端根据持仓自动生成平仓计划。
- **SHFE/INE（上期所、能源中心）** 需同时平今仓和昨仓时，**自动拆成两笔**（先平昨、再平今），每笔有独立 `orderRef`；接口返回**第一笔**委托的 `RtnOrderModel`，`statusMsg` 会包含「已自动拆分为 2 笔」说明。
- 若柜台报「平昨/平今仓位不足」或开平标志类错误，服务端按规则**换开平标志或重试**并换新 `orderRef`（与 App 一致）。
- **非 SHFE/INE** 交易所：直接用通用 `CLOSE`，无自动拆单。

#### 响应 `data`：`RtnOrderModel` 关键字段

```json
{
  "instrumentId": "cu2506",
  "exchangeId": "SHFE",
  "orderRef": "1001",
  "orderSysId": "31574",
  "frontID": 1,
  "sessionId": 123456,
  "direction": "BUY",
  "offsetFlag": "OPEN",
  "limitPrice": 78500.0,
  "volume": 1,
  "volumeTraded": 0,
  "volumeTotal": 1,
  "orderStatus": "SUBMITTED",
  "statusMsg": "已报",
  "insertDate": "20260327",
  "insertTime": "10:15:30",
  "tradingDay": "20260327"
}
```

> **撤单所需字段**：从下单回报中取 `instrumentId`、`exchangeId`、`orderRef`、`orderSysId`、`frontID`（`sessionId` 可选）。请保存整条回报，以便后续撤单。

---

### 10. 撤单

```
POST /open/v1/orders/cancel
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
         Content-Type: application/json
```

撤单成功时响应 `data` 为被撤委托的最新 `RtnOrderModel`（`orderStatus` 变为 `CANCELED`）；撤单失败时 `success=false`，`errorInfo` 有具体原因。

**响应 `data` 示例（撤单成功）：**

```json
{
  "instrumentId": "cu2506",
  "exchangeId": "SHFE",
  "orderRef": "1001",
  "orderSysId": "31574",
  "frontID": 1,
  "sessionId": 123456,
  "direction": "BUY",
  "offsetFlag": "OPEN",
  "limitPrice": 78500.0,
  "volume": 1,
  "volumeTraded": 0,
  "volumeTotal": 1,
  "orderStatus": "CANCELED",
  "statusMsg": "已撤单",
  "cancelTime": "10:20:01",
  "insertDate": "20260327",
  "insertTime": "10:15:30",
  "tradingDay": "20260327"
}
```

#### 请求体（JSON）

```json
{
  "instrumentId": "cu2506",
  "exchangeId": "SHFE",
  "orderRef": "1001",
  "orderSysId": "31574",
  "frontID": 1,
  "sessionId": 123456
}
```

#### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `instrumentId` | string | **是** | 与下单一致 |
| `exchangeId` | string | **是** | 交易所代码，如 `SHFE`、`DCE`、`CZCE`、`INE`、`CFFEX` |
| `orderRef` | string | **是** | 从下单回报的 `orderRef` 取值（实盘由服务端生成） |
| `orderSysId` | string | **是** | 从下单回报的 `orderSysId` 取值 |
| `frontID` | int | **是** | 从下单回报的 `frontID` 取值 |
| `sessionId` | int | 否 | 从下单回报的 `sessionId` 取值；不传则使用当前 CTP 会话 |

---

### 11. 委托回报字段说明（`RtnOrderModel`）

以下是 Agent 最常用的字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `instrumentId` | string | 合约代码 |
| `exchangeId` | string | 交易所代码 |
| `orderRef` | string | 报单引用（撤单时必须用此值） |
| `orderSysId` | string | 交易所报单编号（撤单时必须用此值） |
| `frontID` | int | 前置编号（撤单时必须用此值） |
| `sessionId` | int | 会话编号（撤单时可用此值） |
| `direction` | string | `BUY` / `SELL` |
| `offsetFlag` | string | `OPEN` / `CLOSE` / `CLOSE_TODAY` / `CLOSE_YESTERDAY` |
| `orderStatus` | string | `SUBMITTED`（已报）/ `PART_TRADED_QUEUEING`（部成挂起）/ `ALL_TRADED`（全成）/ `CANCELED`（已撤）等 |
| `volumeTraded` | int | 已成交手数 |
| `volumeTotal` | int | 剩余未成手数 |
| `limitPrice` | number | 报单价格 |
| `statusMsg` | string | 状态描述（含拆单说明、错误信息等） |
| `insertDate` | string | 报单日期，如 `20260327` |
| `insertTime` | string | 报单时间，如 `10:15:30` |
| `tradingDay` | string | 交易日 |

---
