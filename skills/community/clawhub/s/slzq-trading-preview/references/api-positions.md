# Open API · 持仓

> 根地址、`API_BASE`、统一响应与鉴权见 [api.md](./api.md)。

### 6. 持仓列表

```
GET /open/v1/positions?positionDateType=
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

**Query（可选）**

| 参数 | 说明 |
|------|------|
| `positionDateType` | 仅 **`X-Trading-Env: sim`** 生效：传 `今` 或 `昨` 时，仅保留上期所（SHFE）/能源（INE）对应类型的持仓行（与 App `POST /cn/sim/trade/positionList` 的 body 参数一致）。**live 忽略**。 |

**同一 URL 下，`data` 结构随交易环境不同（解析前请先读 `GET /open/v1/me` 的 `tradingEnv` 或请求头）：**

#### 6.1 sim（模拟盘）

与 App「模拟盘 - 查询持仓列表」**同源**：服务端实现为 `getPositionDetailsWithStopLoss` + 上述过滤。`data` 为 **`PositionDetailResponseModel` 数组**（非 CTP 的 `PositionModel`）。

**破坏性说明**：若你曾按旧文档将 sim 的 `data` 当作 `PositionModel` 解析，需改为按下列字段解析。

**每条关键字段（节选）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `positionId` | number | 持仓 ID |
| `instrumentId` | string | 合约代码 |
| `exchangeId` | string | 交易所，如 `SHFE` |
| `direction` / `directionDesc` | number / string | 1 买涨 / 2 买跌 |
| `positionDateType` | string | 上期所/能源：`今` 或 `昨`；其它所汇总行常为 `null` |
| `volume` | int | 该行手数（SHFE/INE 可能拆成今、昨两行） |
| `costPrice` / `openAvgPrice` | number | 开仓均价（展示口径） |
| `currentPrice` | number | 现价 |
| `estimatedProfitLoss` | number | 浮动盈亏（元） |
| `mtmProfit` | number | 盯市盈亏（元），有则返回 |
| `margin` / `commission` | number | 保证金、手续费 |
| `stopLossInfoList` / `stopProfitInfoList` | array | 委托中的止盈止损（与 App 一致） |
| `openDetails` | array | 开仓明细 |

完整字段说明与 App 接口文档一致。

#### 6.2 live（实盘 CTP）

`data` 为 **`PositionModel` 数组**（与 CTP 回报对齐），每条关键字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `instrumentId` | string | 合约代码，如 `cu2506` |
| `posiDirection` | string | `LONG`（多）/ `SHORT`（空） |
| `position` | int | 总持仓手数 |
| `todayPosition` | int | 今仓手数 |
| `ydPosition` | int | 昨仓手数（= position - todayPosition） |
| `openCost` | number | 开仓成本（元），= 成交价×乘数×手数 累计 |
| `openAveragePrice` | number | **开仓均价**（报价单位，如元/吨）= openCost ÷ (乘数 × position)；用于计算浮动盈亏 |
| `positionProfit` | number | 持仓盈亏（元，服务端口径） |
| `useMargin` | number | 占用保证金（元） |
| `tradingDay` | string | 交易日，如 `20260327` |

**live 响应 `data` 示例：**

```json
[
  {
    "instrumentId": "cu2506",
    "posiDirection": "LONG",
    "position": 2,
    "todayPosition": 1,
    "ydPosition": 1,
    "openCost": 157000000,
    "openAveragePrice": 78500.0,
    "positionProfit": 1000.0,
    "useMargin": 39250.0,
    "positionDate": "20260327",
    "tradingDay": "20260327",
    "preSettlementPrice": 78300.0,
    "settlementPrice": 78500.0
  }
]
```

> **live 浮动盈亏估算**：`(lastPrice - openAveragePrice) × volumeMultiple × position`（多头）；空头取负。合约乘数从 `/market/snapshot` 的 `volumeMultiple` 获取。

---
