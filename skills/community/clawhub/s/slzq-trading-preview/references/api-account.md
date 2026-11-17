# Open API · 账户（me / 摘要 / 历史盈亏）

> 根地址、`API_BASE`、统一响应与鉴权见 [api.md](./api.md)。

### 4. 当前密钥上下文与权限档位

```
GET /open/v1/me
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

**响应 `data`：**

```json
{
  "userId": 12345,
  "keyId": 67890,
  "tradingEnv": "sim",
  "scope": "SIM",
  "scopeName": "模拟盘",
  "allowedTradingEnvs": ["sim"],
  "canTradeLive": false,
  "liveUpgradeSteps": [
    "1. 在 App 完成期货实盘登录，使账号关联到 CTP 资金账号。",
    "2. App「我的 → 期货辅助交易」阅读并同意《实盘小龙虾风险告知》。",
    "3. 在同一页面创建密钥时勾选实盘，并填写 CTP 交易密码，服务端校验通过后签发实盘密钥。",
    "4. 用新密钥替换客户端配置中的 API Key，并把交易环境改为 live，然后重启客户端或新开会话。"
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `tradingEnv` | string | **本次请求**生效的交易环境（取自 `X-Trading-Env`） |
| `scope` | string | 权限档位：`SIM`=模拟盘；`SIM_LIVE`=模拟盘+实盘 |
| `allowedTradingEnvs` | string[] | 该密钥允许的交易环境 |
| `canTradeLive` | boolean | 是否可下实盘单；`false` 时用 `live` 会返回 `10412` |
| `liveUpgradeSteps` | string[] | 升级到实盘权限的步骤；已具备实盘权限时为空数组。**直接转述给用户**即可，不要试图从 skill 侧开通 |

档位语义与获取方式详见 [api-auth.md](./api-auth.md)。

---

### 5. 账户摘要

```
GET /open/v1/account/summary
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

> **sim：无需事先在 App 开通模拟盘账户。** 服务端在本接口与 `/open/v1/auth/login` 会自动确保账户已开通（幂等，初始资金取字典配置），拿到密钥即可直接查余额、下模拟单。

**响应 `data`（sim 环境）：**

```json
{
  "tradingEnv": "sim",
  "simAccount": {
    "balance": 1000000.00,
    "available": 980000.00,
    "margin": 20000.00,
    "positionProfit": 500.00
  },
  "liveTradeAccount": null,
  "liveMessage": null
}
```

**响应 `data`（live 环境）：**

```json
{
  "tradingEnv": "live",
  "simAccount": null,
  "liveTradeAccount": {
    "balance": 500000.00,
    "available": 460000.00,
    "margin": 40000.00,
    "positionProfit": -200.00
  },
  "liveMessage": "资金数据来自 CTP；请妥善保管 API Key 与交易环境配置。"
}
```

> live 需已在 App 内绑定实盘 CTP 凭据。

---

### 5.1 账户历史盈亏

```
GET /open/v1/account/pnl/history
Headers: Authorization: Bearer ${API_KEY}
         X-Trading-Env: sim|live
```

**Query（可选）**

| 参数 | 说明 |
|------|------|
| `preset` | `last7d` / `last30d` / `last90d` / `monthToDate`。在**未**传 `startTradingDay`+`endTradingDay` 时生效；默认 `last90d`。语义：`last7d`/`last30d`/`last90d` 为从**当前交易日**起往前推 7/30/90 个**自然日**得到区间起止（按 `yyyyMMdd` 字符串比较，含边界）；`monthToDate` 为**当月 1 日**至当前交易日。 |
| `startTradingDay` | 与 `endTradingDay` **成对**出现；自定义区间，格式 `yyyyMMdd` 或 `yyyy-MM-dd`。若传入则忽略 `preset`。 |
| `endTradingDay` | 同上，结束交易日（含）。 |

**响应 `data` 关键字段：**

| 字段 | 说明 |
|------|------|
| `preset` | 使用的预设；自定义区间时为 `null` |
| `startTradingDay` / `endTradingDay` | 解析后的区间（`yyyyMMdd`） |
| `tradingEnv` | `sim` / `live` |
| `periodTotalProfit` | 区间内各日「平仓盈亏 + 持仓盯市盈亏」之和（元） |
| `periodTotalRate` | 区间收益率（%）：**仅 sim** 为 `periodTotalProfit / 初始资金 × 100`；**live** 为 `null` |
| `liveNote` | **live** 时提示数据来自已落库结算单；**sim** 一般为 `null` |
| `detail` | 与 App 盈亏二级页结构一致：`summary`（收益率汇总）、`dailyData`（日）、`weeklyData`（周）。**sim**：`summary` 为日历口径（今日/本周/本月等），日周序列为区间内裁剪；**live**：`summary` 多为 `null`，日数据来自结算单 `parsedData.accountSummary`（`realizedPL`/`mtmPL`），周汇总由日数据聚合，周收益率在无初始资金口径下为 `0%`。 |

**响应示例（sim，节选）：**

```json
{
  "preset": "last30d",
  "startTradingDay": "20260205",
  "endTradingDay": "20260406",
  "tradingEnv": "sim",
  "periodTotalProfit": 1234.56,
  "periodTotalRate": 1.2345,
  "liveNote": null,
  "detail": {
    "summary": { "todayRate": "+0.10%", "thisWeekRate": "+1.00%" },
    "dailyData": [],
    "weeklyData": []
  }
}
```

