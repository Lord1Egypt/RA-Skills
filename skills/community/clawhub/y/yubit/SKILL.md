---
name: yubit
description: >
  Use this skill whenever the user wants to do anything on the Yubit exchange:
  check prices, query wallet/spot/TradFi/earn/perp balances, transfer funds,
  inspect positions/orders/history/wallet flow records, place or cancel perp
  orders, manage leverage or mode, set take-profit / stop-loss, or troubleshoot
  exchange requests.
license: MIT
metadata: {"author":"yubit","version":"1.0.6","openclaw":{"emoji":"📈","requires":{"bins":["yubit"]},"install":[{"id":"npm","kind":"node","package":"@yubit/exchange-skill","bins":["yubit"],"label":"Install yubit CLI (npm)"}]}}
---

# Yubit

This is the complete Yubit exchange skill.

Use this skill whenever the user wants to do anything on the Yubit exchange.
It keeps the full rule set for market data, wallets, spot, TradFi, earn,
perpetual futures trading, and diagnostics in one place.

Use the yubit MCP tools for all exchange operations. Do not guess balances,
prices, positions, order state, or write success.

## Market

Use the yubit MCP tools for all market-data queries.
Never use web search for price or market data.

## Rules

1. For ANY price, market, or exchange quote query, use the yubit MCP tools.
   - Prices
   - 24h change
   - bid / ask
   - mark price
   - funding
   - orderbook
   - recent trades
   - kline / candlestick history
   - contract rules
   - leverage brackets / risk tiers

2. Do not guess or fabricate market data. If a tool call fails, report the error.
   - If the user wants the exact raw context, use the diagnostics tools in this skill with `traceId`.

3. Symbol mapping:
   - BTC / btc → `BTCUSDT`
   - ETH / eth → `ETHUSDT`
   - SOL / sol → `SOLUSDT`
   - BTC FreeU / btc freeu → `BTCFreeU`
   - ETH FreeU / eth freeu → `ETHFreeU`

4. For kline queries:
   - Use `getKlines` for normal last-price candles.
   - Use `getMarkPriceKlines` only when the user explicitly asks about mark-price history instead of normal last-price candles.
   - `start` and `end` must be passed together.
   - `getMarkPriceKlines.limit` max is `200`.

5. Use `getRiskLimits` when the user asks about:
   - leverage brackets
   - risk tiers
   - max notional per tier
   - liquidation thresholds

6. Use `getInstruments` when the user asks about:
   - min/max order size
   - tick size / price precision
   - leverage range
   - contract trading status

7. Funding-related queries:
   - Current funding or next settlement → `getFundingRate`
   - Historical funding trend → `getFundingRateHistory`

8. Orderbook / trade-flow queries:
   - Bid/ask depth, spread, walls → `getOrderbook`
   - Recent prints / tape / latest public trades → `getRecentTrades`

9. Timestamp format:
   - All time fields in MCP responses are formatted as `YYYY-MM-DD HH:MM:SS±HH:MM`, not Unix epoch.
   - Example: `2026-04-10 17:00:00+08:00`
   - When showing times to the user, use the formatted string directly — do not convert again.

10. If the user asks for "all visible contracts", "all instruments", or "all risk tiers", you may omit `symbol`.
    - For large result sets, mention that the response may be paginated.

11. If the user asks a market question and the current session exposes no relevant tool, call `getCapabilities()` first and report what this MCP server can do in the current session.

## Parameter mapping

- BTC / btc → `BTCUSDT`
- ETH / eth → `ETHUSDT`
- SOL / sol → `SOLUSDT`
- BTC FreeU / btc freeu → `BTCFreeU`
- ETH FreeU / eth freeu → `ETHFreeU`

## Tools available

- `getTicker(symbol)` — price, 24h change, volume, funding rate
- `getOrderbook(symbol)` — bid/ask depth
- `getKlines(symbol, interval, limit?, start?, end?)` — last-price candlestick data (OHLCV). `start`/`end` are ms timestamps and must come as a pair.
- `getMarkPriceKlines(symbol, interval, limit?, start?, end?)` — mark-price candlestick data (OHLC only, no volume/turnover). `limit` max 200.
- `getFundingRate(symbol)` — current funding rate
- `getFundingRateHistory(symbol, limit?, startTime?, endTime?)` — historical funding rates, optional ms time range
- `getInstruments(symbol?, status?, limit?, cursor?)` — contract specs and trading status
- `getRiskLimits(symbol?)` — risk-limit tiers per contract
- `getRecentTrades(symbol)` — recent public trades
- `getCapabilities()` — capability snapshot for the current MCP session

## Wallet

Use the yubit MCP tools for all account and portfolio queries.

## Rules

1. Account semantics:
   - `perpGetBalance` is CONTRACT account balance (for perpetual futures trading).
   - `spotGetBalance` is SPOT account asset balances.
   - `tradfiGetBalance` is TradFi account detail query.
   - `earnGetBalance` is earn/perfi account balance query.
   - `fundGetAssets` is FUND account asset balances.
   - `getPortfolioNetWorth` is total value across fund + contract + spot + tradfi in USDT equivalent.
   - If the user says only "余额", clarify whether they want contract balance, spot balance, TradFi balance, earn balance, fund wallet assets, or total wallet value.

2. `perpGetPositions` requires either:
   - `symbol`, or
   - `settleCoin`
   Do NOT call `perpGetPositions` without any parameter.

3. To see ALL positions across all settle coins, query USDT and FreeU separately.

4. `perpGetOpenOrders` requires at least one of:
   - `symbol`
   - `settleCoin`
   - `baseCoin`

5. Use `perpGetModeConfigs` when the user asks:
   - current leverage
   - cross vs isolated
   - merged vs separate
   - current account mode without open positions

6. Position and margin modes:
   - 全仓 (Cross): `tradeMode=0`, `tradeModeLabel=Cross`
   - 逐仓 (Isolated): `tradeMode=1`, `tradeModeLabel=Isolated`
   - 合仓 (Merged): `isSeparatePz=false`, positions in `list`
   - 分仓 (Separate): `isSeparatePz=true`, positions in `separateList`, each with unique `pzLinkId`

7. Contract record queries:
   - `perpGetOrderHistory` = historical orders
   - `perpGetExecutions` = fills / executions
   - `perpGetClosedPnl` = closed-position PnL
   - `perpGetWalletFlowRecords` = wallet flow / bills such as transfers, realized PnL, funding fees, and trading fees
   - `perpGetOrderHistory`, `perpGetExecutions`, `perpGetClosedPnl` require `symbol`
   - If the user does not specify a symbol, ask before calling
   - `perpGetWalletFlowRecords` does not require `symbol`; use `coin='USDT'` when the user is asking about USDT contract wallet bills
   - `baseCoin` can broaden some queries, but `symbol` is still the safest default

8. Use `perpGetOpenOrders(orderFilter='StopOrder')` when the user asks about:
   - TP/SL sub-orders
   - trailing-stop sub-orders
   - trigger / conditional orders
   - why a stop order did not trigger yet

9. Use `perpGetModeConfigs` before giving an authoritative answer about:
   - current leverage
   - cross / isolated
   - merged / separate
   - account configuration when there is no open position

10. Timestamp format:
   - All time fields in MCP responses are formatted as `YYYY-MM-DD HH:MM:SS±HH:MM`
   - Use the formatted string directly when replying

11. If an account/order query fails and the user wants exact raw context, use the diagnostics tools in this skill with the returned `traceId`.

12. Treat `getCapabilities()` and the registered tool list as the source of truth for account-query scope in the current session.
    - Do not promise unsupported account modules based on future plans.
    - If a requested account type has no tool, state that clearly.

13. Transfer rules:
   - Use `transfer(coin, amount, fromWallet, toWallet)` for wallet-to-wallet transfers.
   - Wallet mapping:
     - `FUNDING` = fund wallet (`fundGetAssets`)
     - `TRADING` = perp/contract wallet (`perpGetBalance`)
     - `SPOT` = spot wallet (`spotGetBalance`)
     - `TRADFI` = TradFi wallet (`tradfiGetBalance`)
   - Post-verify rule for every transfer:
     - `FUNDING` side → read back with `fundGetAssets()`
     - `TRADING` side → read back with `perpGetBalance(coin='<settle coin>')`
     - `SPOT` side → read back with `spotGetBalance()`
     - `TRADFI` side → read back with `tradfiGetBalance()`
   - Only say "划转成功" after confirming the source balance decreased and destination balance increased by the expected amount.
   - If the write returns success but the balances do not match on read-back, say the transfer request was accepted but not yet verified, and include the `traceId`.

## Parameter mapping

- FreeU 合约余额 → `perpGetBalance(coin='FreeU')`
- 现货余额 → `spotGetBalance()`
- TradFi 余额 → `tradfiGetBalance()`
- 理财余额 → `earnGetBalance()`
- 资金账户余额 → `fundGetAssets()`
- 全部钱包总资产 → `getPortfolioNetWorth()`
- 资金账户划到合约账户 → `transfer(coin='USDT', amount='数量', fromWallet='FUNDING', toWallet='TRADING')`
- 资金账户划到现货账户 → `transfer(coin='USDT', amount='数量', fromWallet='FUNDING', toWallet='SPOT')`
- 合约账户划到现货账户 → `transfer(coin='USDT', amount='数量', fromWallet='TRADING', toWallet='SPOT')`
- 资金账户划到 TradFi 账户 → `transfer(coin='USDT', amount='数量', fromWallet='FUNDING', toWallet='TRADFI')`
- TradFi 划回资金账户 → `transfer(coin='USDT', amount='数量', fromWallet='TRADFI', toWallet='FUNDING')`
- FreeU 持仓 → `perpGetPositions(settleCoin='FreeU')`
- FreeU 挂单 → `perpGetOpenOrders(settleCoin='FreeU')`
- 某个 base coin 的所有挂单（跨 USDT 和 FreeU）→ `perpGetOpenOrders(baseCoin='BTC')`
- 合约资金流水 / 账单流水 → `perpGetWalletFlowRecords(coin='USDT', limit='20', sort='DESC')`
- 合约手续费流水 → `perpGetWalletFlowRecords(coin='USDT', fundType='4', limit='20', sort='DESC')`
- 合约已实现盈亏流水 → `perpGetWalletFlowRecords(coin='USDT', fundType='2', limit='20', sort='DESC')`

## Tools that require symbol or settleCoin

These tools need at least a `symbol` or `settleCoin`. If the user does not specify, ask before calling:
- `perpGetFeeRate` — requires `symbol`
- `perpGetOpenOrders` — pass `symbol` or `settleCoin` or `baseCoin`
- `perpGetOrderHistory`, `perpGetExecutions`, `perpGetClosedPnl` — requires `symbol`

## Error handling

- If `perpGetPositions` fails with missing parameter context, add `symbol` or `settleCoin` and retry.
- If `perpGetOpenOrders` returns empty under the default filter but the user expects TP/SL or trigger orders, retry with `orderFilter='StopOrder'`.
   - If the user wants the exchange's exact raw request/response, use the diagnostics tools in this skill with `traceId`.

## Tools available

- `perpGetBalance(coin?)` — CONTRACT account balance
- `perpGetPositions(symbol?, settleCoin?, limit?, cursor?)` — open positions
- `perpGetModeConfigs(symbol?, coin?, category?)` — current leverage and mode configs
- `perpGetFeeRate(symbol)` — maker/taker fee rates
- `perpGetOpenOrders(symbol?, settleCoin?, baseCoin?, orderId?, orderLinkId?, orderFilter?, limit?, cursor?)` — active orders
- `perpGetOrderHistory(symbol, ...)` — historical orders
- `perpGetExecutions(symbol, ...)` — executions / fills
- `perpGetClosedPnl(symbol, ...)` — closed PnL
- `perpGetWalletFlowRecords(coin?, startTime?, endTime?, limit?, fundType?, cursor?, sort?, includeFreeU?)` — perp wallet flow / bill records. `startTime` / `endTime` use Unix seconds, not milliseconds
- `spotGetBalance()` — SPOT account asset balances
- `tradfiGetBalance()` — TradFi account details
- `earnGetBalance()` — earn/perfi account balances
- `fundGetAssets()` — FUND account asset balances
- `getPortfolioNetWorth()` — total balance across all wallets
- `transfer(coin, amount, fromWallet, toWallet)` — wallet transfer; see Rule 13 for read-back requirements
- `getCapabilities()` — capability snapshot for the current MCP session

## Spot

Use the yubit MCP tools for all spot-account queries.

## Rules

1. Account semantics:
   - `spotGetBalance` is SPOT account asset list.
   - It is NOT the funding wallet (`fundGetAssets`) and NOT the perp account (`perpGetBalance`).
   - If the user says only "现货余额" or "现货账户", use `spotGetBalance`.

2. `spotGetBalance` currently returns the full spot asset list for the current account.
   - The response contains per-coin fields such as total, free, locked, and valuation fields.
   - If the user only wants non-zero spot balances, filter locally after retrieval.

3. Do not guess or fabricate spot balances.
   - If the tool call fails, report the error directly.
   - If the user wants the exact raw exchange response, use the diagnostics tools in this skill with `traceId`.

4. Treat `getCapabilities()` and the registered tool list as the source of truth for current spot coverage.
   - Current spot support is query-only.
   - Do not promise spot order placement, spot order history, or spot trade actions unless those tools are actually exposed.

5. Timestamp format:
   - If the response includes formatted time fields, use them directly.
   - Do not convert the returned strings again.

## Parameter mapping

- 现货余额 / 现货账户余额 / spot balance → `spotGetBalance()`
- 现货可用余额 / 现货可用资金 → 先 `spotGetBalance()`，再看 `free`
- 现货冻结余额 / 现货挂单占用 → 先 `spotGetBalance()`，再看 `locked`
- 现货有哪些币有余额 → 先 `spotGetBalance()`，只保留 `total > 0` 的币种

## Error handling

- If the user asks for a single coin's spot balance, still call `spotGetBalance()` first and then filter locally.
- If the user asks for spot trading actions, state that the current MCP session only exposes spot account query, not spot trading.

## Tools available

- `spotGetBalance()` — SPOT account asset balances (per-coin total, free, locked, valuation fields)
- `getCapabilities()` — capability snapshot for the current MCP session

## TradFi

Use the yubit MCP tools for all TradFi-account queries.

## Rules

1. Account semantics:
   - `tradfiGetBalance` is the TradFi account detail query.
   - It is NOT the funding wallet (`fundGetAssets`), NOT the spot account (`spotGetBalance`), and NOT the perp account (`perpGetBalance`).
   - If the user says only "TradFi 余额" or "MT5 账户", use `tradfiGetBalance`.

2. `tradfiGetBalance` currently returns a single account-detail object for the current account.
   - Common fields include `balance`, `equity`, `margin`, `margin_free`, `margin_level`, `margin_leverage`, `storage`, `floating`, and `login`.
   - If `login` is `0`, treat it as "account not opened yet" unless the backend says otherwise.

3. Do not guess or fabricate TradFi balances.
   - If the tool call fails, report the error directly.
   - If the user wants the exact raw exchange response, use the diagnostics tools in this skill with `traceId`.

4. Treat `getCapabilities()` and the registered tool list as the source of truth for current TradFi coverage.
   - Current TradFi support is query-only.
   - Do not promise TradFi order placement or TradFi history queries unless those tools are actually exposed.

## Parameter mapping

- TradFi 余额 / TradFi 账户 / MT5 账户详情 → `tradfiGetBalance()`
- TradFi 可用保证金 → 先 `tradfiGetBalance()`，再看 `margin_free`
- TradFi 净值 → 先 `tradfiGetBalance()`，再看 `equity`
- TradFi 浮动盈亏 → 先 `tradfiGetBalance()`，再看 `floating`

## Error handling

- If the user asks for TradFi trading actions, state that the current MCP session only exposes TradFi account query, not TradFi trading.
- If the user asks whether TradFi is opened, use `tradfiGetBalance()` first and inspect `login` / returned fields before answering.

## Tools available

- `tradfiGetBalance()` — TradFi account details (balance, equity, margin, margin free, margin level, leverage, floating PnL, login)
- `getCapabilities()` — capability snapshot for the current MCP session

## Earn

Use the yubit MCP tools for all earn-account queries.

## Rules

1. Account semantics:
   - `earnGetBalance` is the earn/perfi account balance query.
   - It is NOT the funding wallet (`fundGetAssets`), NOT the spot account (`spotGetBalance`), and NOT the perp account (`perpGetBalance`).
   - If the user says "理财余额" or "Earn 账户", use `earnGetBalance`.

2. `earnGetBalance` currently returns the current earn account rows for the account.
   - Common row fields include `symbol`, `balance`, `equity`, `total_swap`, and `yesterday_swap`.
   - If the response is empty, say there are currently no earn-account rows instead of inventing zero positions.

3. Do not guess or fabricate earn balances or yields.
   - If the tool call fails, report the error directly.
   - If the user wants the exact raw exchange response, use the diagnostics tools in this skill with `traceId`.

4. Treat `getCapabilities()` and the registered tool list as the source of truth for current earn coverage.
   - Current earn support is query-only.
   - Do not promise earn subscribe/redeem actions unless those tools are actually exposed.

## Parameter mapping

- 理财余额 / earn balance / perfi 余额 → `earnGetBalance()`
- 理财净值 → 先 `earnGetBalance()`，再看每个币种的 `equity`
- 理财累计收益 / 累计利息 → 先 `earnGetBalance()`，再看 `total_swap`
- 理财昨日收益 → 先 `earnGetBalance()`，再看 `yesterday_swap`

## Error handling

- If the user asks for a single coin's earn balance, still call `earnGetBalance()` first and then filter locally.
- If the user asks for earn subscribe / redeem actions, state that the current MCP session only exposes earn account query, not earn trading actions.

## Tools available

- `earnGetBalance()` — earn/perfi account balances and interest fields
- `getCapabilities()` — capability snapshot for the current MCP session

## Diagnostics

Use this skill for capability discovery and deep troubleshooting.

## Rules

1. If you are unsure what tools are currently available, call `getCapabilities` first.

2. When the user asks what this MCP can do, what tools are available, or what capabilities are enabled:
   - Call `getCapabilities()` first.
   - Then use the registered tool list as the source of truth for exact tool names.
   - Reply in the user's language.
   - If the user asks in Chinese, reply in Chinese.
   - If the user asks in English, reply in English.
   - Do not dump only raw tool names. Add a short user-facing description for each tool or tool group.
   - Keep the description practical: `tool name + what it does + key boundary if needed`.
   - Do not rewrite or localize the tool names themselves.

3. Every MCP tool response includes a `traceId`.

4. When the user asks for:
   - raw exchange request/response
   - exact error context
   - debugging a failed tool call
   use `getTrace(traceId)` or `searchTraces(...)`.

5. For failed order/trade operations, always surface the `traceId`.

6. Do not guess root cause when the trace can answer it directly.

7. `getCapabilities()` is the source of truth for the current session:
   - whether auth is configured
   - whether trade write tools are enabled
   - how many tools are currently registered
   - which modules are active

8. `searchTraces(...)` supports:
   - `traceId`
   - `orderId` / `orderNo`
   - `orderLinkId`
   - `symbol`
   - `toolName`
   - `success`
   - `fromTs` / `toTs`

9. `getCapabilities()` returns a machine-readable snapshot of:
   - `hasAuth`
   - `canTrade`
   - `toolCount`
   - `modules`

10. If the user is troubleshooting a write op:
   - start from the returned `traceId`
   - inspect the normalized MCP response
   - then inspect the raw exchange HTTP request/response
   - only after that summarize the root cause

## Main tools

- `getCapabilities`
- `getTrace`
- `searchTraces`

## Perpetual Futures

Use the yubit MCP tools for all exchange queries and trading operations.
Never use web search for price or market data.

This skill intentionally keeps the original dense trading rules.

## Rules

1. For ANY price, market, or exchange query, use the yubit MCP tools.

2. Place orders directly when the user gives a clear instruction.
   For market orders, briefly note: "Market orders execute immediately and cannot be cancelled."

3. Closing positions:
   - **全部平仓**: `perpClosePosition(symbol, positionIdx)` — closes the ENTIRE position, no qty parameter.
   - **部分平仓**: Use `perpCreateOrder(side=反向, qty=部分数量, reduceOnly=true)`.
     Example: holding 0.3 BTC Long, close 0.12 → `perpCreateOrder(symbol=BTCUSDT, side=Sell, orderType=Market, qty=0.12, positionIdx=1, reduceOnly=true)`.
   - **分仓模式下部分平仓**: 必须先查 `perpGetPositions` 获取目标仓位的 `pzLinkId`，然后 `perpCreateOrder` 带上 `pzLinkId` 确保减正确的仓位。
   - When the user specifies a qty less than the full position, MUST use `perpCreateOrder` with `reduceOnly=true`. Do NOT use `perpClosePosition` for partial close.

3a. **加仓到既有仓位（合仓 / 分仓都适用）**: 用户说"加仓 BTC 多单 100 U"这类意图时：
   - **优先使用 `perpAddToPosition(symbol, positionIdx, qty, pzLinkId?)`**。这是专门给“加仓既有仓位”设计的安全路径：
     - 分仓模式下会自动命中唯一仓位或要求显式 `pzLinkId`
     - 合仓模式下不需要 `pzLinkId`，同方向会合并到单一仓位
     - 两种模式都会回读验证实际结果
   - 如果因为特殊需求必须走底层 `perpCreateOrder`，先 `perpGetPositions(symbol)` 找到目标仓位，记下它的 `pzLinkId` **和** `leverage`
   - `perpCreateOrder(..., pzLinkId=<目标仓位的 pzLinkId>)` —— **不传 pzLinkId 会被 runtime 视为开新分仓**（每个 pzLinkId 是一个独立子仓位，这是设计而不是 bug）
   - **加仓前不要调用 `perpSetLeverage`**：分仓仓位的杠杆和 pzLinkId 是绑定的，中途改杠杆会导致下一单开成一个新的独立分仓（不同 leverage 不会合并）。如果用户确实要改杠杆，应当先平掉该仓位再改杠杆再开新仓位。
   - 如果同方向已有 **多个** 分仓仓位，而用户没有明确目标 `pzLinkId`，**必须先把候选仓位列出来让用户选**；不要默认挑一个。

4. When querying positions, you MUST pass either `symbol` or `settleCoin`:
   - With a specific symbol: pass `symbol` (e.g. `BTCUSDT`, `ETHFreeU`)
   - For all positions under a settle coin: pass `settleCoin` (e.g. `USDT`, `FreeU`)
   - To see ALL positions across all coins, query USDT and FreeU separately.
   - Do NOT call `perpGetPositions` without any parameter — it will return an error.

5. When the account uses separate positions (multiple positions for same direction),
   `perpClosePosition` without `pzLinkId` will close ALL positions of that direction.
   Show the user all positions and let them choose, or pass `pzLinkId` to target one.

6. Creating TP/SL requires a strict sequence:
   a. Call `perpGetPositions` first to get the target position.
   b. If the position has `isSeparatePz=true`, you MUST extract its `pzLinkId`.
   c. Call `perpCreateTpSl` with symbol + positionIdx + tpSlMode + pzLinkId + takeProfit/stopLoss.
   d. After `perpCreateTpSl` returns success, call `perpGetPositions` again to verify.
   e. Only confirm to user when takeProfit/stopLoss in the response are non-zero.
   f. If still 0.0, tell user "setting submitted but not confirmed, may need retry".
   g. Advanced TP/SL: pass `tpOrderType='Limit' + tpLimitPrice` for limit-price TP, or `slOrderType='Limit' + slLimitPrice` for limit-price SL.
   h. Partial TP/SL: pass `tpSlMode='Partial' + tpSize/slSize`.
   h1. `tpSlMode='Full'` means **full-position TP/SL scope**, not Cross margin mode. Do not describe it as "全仓 Cross".
   i. Trailing stop (移动止盈止损 / 追踪止损):
      - Hard-required: `isMovingTpSl=true` + `tpSlMode='Full'` + `retracePercentage` (backend rejects without it).
      - **`retracePercentage` is DECIMAL form**, NOT a percentage number. To express 0.5% retrace pass `"0.005"`. To express 1% pass `"0.01"`. Valid range `[0.001, 1.0)` meaning 0.1% to just under 100%.
      - `movingTriggerBy` is optional (gateway defaults to `LastPrice` if omitted); if you pass it, it must be `LastPrice` or `MarkPrice`.
      - `movingActivationPrice` is optional. If omitted, the sub-order is immediately live at the current market price (status `Untriggered`). If passed with a future price (above current for long, below for short), the sub-order is `Unactivated` and only starts trailing once market reaches that price. `perpReplaceTpSl` only modifies `Unactivated` orders — if you need to amend the trailing stop after creation, pass an explicit future `movingActivationPrice` at creation time.
      - `retracePercentage` drives the dynamic trailing trigger math and is always required. `movingTpSlSize` lets you set the qty for the trailing stop. `retraceDelta` is passed through and stored on the sub-order but is **not consumed by the current trigger logic** — it is not a working substitute for `retracePercentage`, and when both are passed the runtime computes the trigger purely from `retracePercentage` (verified by real-MCP experiment: `triggerPrice = base × (1 − retracePercentage)`, `retraceDelta` ignored). All four are passed through by this skill for forward compatibility.
      - Each position can hold only **one** moving TP/SL at a time. Creating a second while one exists returns exchange error code `14120005 Invalid Parameter` — this is a reliable indirect proof that the first one persisted.
      - A moving TP/SL is an **independent stop sub-order**. It does NOT update `position.trailingStop` / `position.activePrice` (those belong to the legacy `setTradingStop` path and stay zero).
      - **Querying a moving TP/SL sub-order**: both `Untriggered` (created without an activation price → immediately live) and `Unactivated` (created with a future activation price, waiting to reach it) moving TP/SL sub-orders appear in `perpGetOpenOrders` under the default filter and under `orderFilter='StopOrder'`, with `stopOrderType='MovingTpSl'` and `orderStatus` set to `Untriggered` / `Unactivated` respectively. For `Untriggered` orders the `triggerPrice` field holds the current dynamic trailing trigger (e.g. `base × (1 - retracePercentage)` for long); for `Unactivated` orders `triggerPrice` is empty string (the activation price is stored elsewhere and is not echoed on this field). Creating a second moving TP/SL on the same position while one exists returns `14120005 Invalid Parameter`.
   j. Modifying existing TP/SL:
      - Find the sub-order `orderId` via `perpGetOpenOrders(symbol, orderFilter='StopOrder')`, then call `perpReplaceTpSl(symbol, orderId, ...)`.
      - For a trailing stop (moving TP/SL) sub-order, `perpReplaceTpSl` only works while the order is `Unactivated` (created with a future activation price that has not yet been reached). Once the trailing stop is `Untriggered` / activated, `perpReplaceTpSl` returns `14120040 moving tp sl order status is not unactivated` — cancel and re-create instead.
      - `perpReplaceTpSl` accepts `movingTriggerBy` / `movingActivationPrice` / `retracePercentage` / `retraceDelta` / `movingTpSlSize` (same decimal-form rule for `retracePercentage`). You cannot convert a regular TP/SL into a trailing stop via replace (`isMovingTpSl` is not part of the replace request).
      - Do NOT use `perpCreateTpSl` to modify existing TP/SL — use `perpReplaceTpSl`.
   k. **"收益 N%" / "10% 止盈" 这类模糊措辞的默认解释**: 当用户说"盈利 10% 止盈" / "亏损 5% 止损" 等百分比但没有明确"相对于什么"时，**默认按 margin (positionBalance) 百分比解释**（等价于 ROE%，杠杆影响通过 positionBalance 间接进入公式）：
      - 多单止盈: `TP = entry + (positionBalance × pct) / qty`
      - 多单止损: `SL = entry − (positionBalance × pct) / qty`
      - 空单对称互换
      - "绝对金额"场景（例如"盈利 10 U 止盈"）用 `TP = entry ± amount / qty`，和杠杆无关
      - "名义价值百分比" (e.g. "BTC 涨 10% 止盈") 用 `TP = entry × (1 ± pct)`
      - **如果上下文无法确定是哪一种，主动问一次**，不要默默猜测。

6a. **配置型写操作先查当前状态，避免无意义写操作**:
   - 对 `perpSetLeverage`、`perpSwitchMarginMode`、`perpSwitchPositionMode`，先调用 `perpGetModeConfigs(symbol)`（或按需 `perpGetModeConfigs(coin='USDT')`）确认当前配置。
   - 如果当前已经是目标状态，就直接告诉用户当前已是该配置，不要重复提交写操作。
   - 批量操作和重复执行场景尤其要遵守这一条，避免把无变化写操作提交成无意义请求。

7. **Write operations must be post-verified, do NOT confirm success on `code: 0` alone.** Any write op (`perpCreateOrder`, `perpAddToPosition`, `perpCreateTpSl`, `perpReplaceTpSl`, `perpModifyOrder`, `perpAddMargin`, `perpClosePosition`, `perpSetLeverage`, `perpSwitchMarginMode`, `perpSwitchPositionMode`) returning `success: true` means "the request was accepted", NOT "the intended state was achieved". Before telling the user "成功", you MUST read back and verify the actual state:
   - **下单 / 加仓**:
     - `perpCreateOrder`: call `perpGetOpenOrders` (if limit/trigger) or `perpGetPositions` (if market — check size / direction / pzLinkId / entryPrice match intent).
     - `perpAddToPosition`: prefer this over raw `perpCreateOrder` for "加仓已有仓位". It already resolves the target position and performs post-verification; still report the returned `targetPzLinkId` / `afterSize` back to the user.
     - For **conditional / trigger orders**, the resulting order must appear under `orderFilter='StopOrder'` with the correct `triggerPrice` / `triggerDirection` — if not, the request likely fell back to a non-trigger order type.
     - For **加仓到既有分仓**, verify that `separateList` did NOT grow by a new entry, `pzLinkId` stayed on the intended target position, and `size` increased exactly by the requested add-on quantity. If any of those checks fail, stop the flow and report the mismatch; do not continue to TP/SL or close steps.
     - **Market 开仓后如果 `perpGetPositions(symbol)` 为空**: do NOT jump to "symbol 映射" or "仓位同步延迟" first. You MUST diagnose in this order:
       1. `perpGetOrderHistory(symbol, orderId/orderLinkId)` — confirm the open order really reached `Filled`
       2. `perpGetExecutions(symbol, orderId/orderLinkId)` — capture actual fill qty / fill price / execTime
       3. `perpGetClosedPnl(symbol, limit='10')` — look for a near-immediate opposite-side close with matching `closedSize` and recent timestamp
       4. If a matching close exists, report "开仓后已被后续平仓单平掉", and if available include the close order's `reduceOnly` evidence from `perpGetOrderHistory`
       5. Only if no matching close is found after one short retry may you say "仓位为空但未定位到匹配平仓记录"
     - `perpGetOrderHistory` may show exchange-local symbols such as `M1ETHUSDT`; treat that as exchange-side history representation, not proof that the position is hidden under another query symbol.
   - **设置 TP/SL**:
     - `perpCreateTpSl` (regular TP/SL): call `perpGetPositions(symbol)` and check `takeProfit` / `stopLoss` / `tpSlMode` actually reflect the new values.
     - Also call `perpGetOpenOrders(symbol, orderFilter='StopOrder')` and check the sub-order `triggerPrice` matches your intent.
     - **Full 模式下的 silent-no-op**：在 `tpSlMode=Full` 路径下，如果 position 已有 TP/SL 子单，再次 `perpCreateTpSl` 会被 runtime 接受（`success: true`）但**不修改已有子单**（2026-04-11 实测：`updatedTime` 移动但 `triggerPrice` 不变）。要修改已有 Full TP/SL，必须走 `perpReplaceTpSl(orderId, ...)` 路径（Rule 6j）。
     - **Partial 模式不同**：在 `tpSlMode=Partial` 路径下，再次 `perpCreateTpSl` 会**新增**一组子单（不是 no-op），一个 position 可以挂多组 Partial TP/SL。所以 Partial 模式下如果用户意图是"修改"而非"追加"，同样应该先找到子单 orderId 再 `perpReplaceTpSl`。
   - **修改 TP/SL**:
     - `perpReplaceTpSl`: after calling, read the sub-order back via `perpGetOpenOrders(orderFilter='StopOrder')` and confirm the target field (`triggerPrice` / moving params) actually changed on the **same** `orderId`.
     - `perpCreateTpSl` / `perpReplaceTpSl` (moving TP/SL): verify via `perpGetOpenOrders(symbol, orderFilter='StopOrder')` that a sub-order with `stopOrderType='MovingTpSl'` and matching `orderStatus` appears.
   - **改单 / 保证金调整**:
     - `perpModifyOrder`: read the order back via `perpGetOpenOrders` and confirm the modified field (price / qty / triggerPrice / TP / SL) actually changed.
     - `perpAddMargin`: call `perpGetPositions` and check `positionBalance` delta matches the requested margin delta.
   - **平仓 / 部分平仓**:
     - `perpClosePosition`: call `perpGetPositions` and confirm the target `pzLinkId` / `positionIdx` no longer appears (or has size 0). Then follow the **post-close P&L enrichment** flow below.
     - `perpCreateOrder(reduceOnly=true)` (partial close): call `perpGetPositions` and confirm position size decreased by the expected qty. Then follow the **post-close P&L enrichment** flow below.
     - **Post-close P&L enrichment** (applies to both full close and partial close):
       - After confirming the close succeeded, query `perpGetClosedPnl(symbol, limit='5')` and match the most recent record by symbol + close direction + closedSize + recent timestamp.
       - Present to the user:
         - `closedPnl` (已结盈亏)
         - `avgEntryPrice` (入场均价)
         - `avgExitPrice` (出场均价)
         - `closedSize` (平仓数量)
       - If the user also asks for fees, query `perpGetExecutions(symbol, limit='5')` and sum `execFee` for the matching orderId(s).
       - If the first query returns no matching record (eventual consistency), wait ~1 second and retry once. If still no match, confirm "平仓成功" but state "已结盈亏记录暂未查询到，可稍后用 perpGetClosedPnl 查看"。Do NOT fabricate P&L numbers.
   - **配置类写操作**:
     - `perpSwitchMarginMode` / `perpSwitchPositionMode`: call `perpGetModeConfigs(symbol)` (or `perpGetPositions` if a position exists) and confirm `tradeMode` / `isSeparatePz` match the new setting.
     - `perpSetLeverage`: call `perpGetModeConfigs(symbol)` and confirm `buyLeverage` / `sellLeverage` match the new setting (works even without open positions). For per-position leverage (with `pzLinkId`), also check `perpGetPositions(symbol)` to verify the target position's `leverage` field updated.
   - **通用规则**:
     - **Eventual consistency**: some write ops (especially `perpClosePosition`, `perpCancelOrder`, `perpSwitchMarginMode`) have a short propagation delay — the first read-back may still show the old state. If the first verification does not match, wait ~1 second and retry **once** before concluding mismatch. Two consecutive mismatches = real failure.
     - **On confirmed mismatch**: NEVER silently tell user "success". Surface the `traceId` and either retry via the correct path (e.g. switch from `perpCreateTpSl` to `perpReplaceTpSl` when TP/SL already exists) or tell the user the request didn't take effect.

8. Do not guess or fabricate exchange data. If a tool call fails, report the error.
   - Every MCP tool response includes a `traceId`.
   - When the user asks for diagnostics details, raw MCP request/response, or exact exchange error context, use `getTrace(traceId)` or `searchTraces(...)`.
   - For failed order/trade operations, include the `traceId` in your reply so the user can inspect the exact raw exchange response later.

8a. When the user asks to "查合约记录" / "查账单" / "查手续费流水" / "查划转流水", first identify which record class they mean:
   - historical orders → `perpGetOrderHistory`
   - executions / fills → `perpGetExecutions`
   - closed-position PnL → `perpGetClosedPnl`
   - wallet flow / bills → `perpGetWalletFlowRecords`
   If the intent is ambiguous, ask which one they want. Do not silently pick the wrong record type.

9. `positionIdx=1` for Long, `positionIdx=2` for Short. Always pass `positionIdx` when placing orders or closing positions.

10. Position and margin modes (from `perpGetPositions` response):
   - **全仓 (Cross)**: `tradeMode=0`, `tradeModeLabel=Cross`. Shared margin across positions.
   - **逐仓 (Isolated)**: `tradeMode=1`, `tradeModeLabel=Isolated`. Each position has independent margin.
   - **合仓 (Merged)**: `isSeparatePz=false`. Positions appear in `list`. Same direction merges into one position. No `pzLinkId` needed.
   - **分仓 (Separate)**: `isSeparatePz=true`. Positions appear in `separateList`. Same direction can have multiple positions, each with unique `pzLinkId`.
   - When operating on positions, always check `isSeparatePz` first:
     - If `false` (合仓): pass `positionIdx` only, no `pzLinkId` needed.
     - If `true` (分仓): pass both `positionIdx` and `pzLinkId` for `perpClosePosition`, `perpCreateTpSl`, and partial close (`perpCreateOrder + reduceOnly`).

11. Batch operations safety:
    - `perpCancelAllOrders` and `perpClosePosition` with `settleCoin` affect ALL symbols under that coin.
    - Using `settleCoin` without `symbol` requires `confirmBatch=true` — the tool will reject without it.
    - Always prefer `symbol` for targeted operations.
    - Only use `settleCoin` + `confirmBatch=true` when the user explicitly asks to operate on ALL positions/orders under a coin (e.g. "cancel all FreeU orders", "close all FreeU positions").

12. Timestamp format:
    - All time fields in MCP responses are formatted as `YYYY-MM-DD HH:MM:SS±HH:MM` with timezone offset, not Unix epoch.
    - Example: `2026-04-10 17:00:00+08:00`. The offset reflects the MCP Server host's local timezone — the string is self-describing.
    - Covered fields: `createdTime`, `updatedTime`, `execTime`, `createdAt`, `fundingRateTimestamp`, `nextFundingTime`, `launchTime`, `deliveryTime`.
    - When showing times to the user, use the formatted string directly — do not convert again.

13. Conditional / trigger orders (`perpCreateOrder` with `triggerPrice`):
    - **Required pair**: `triggerPrice` + `triggerDirection` must be set together. Passing `triggerPrice` without `triggerDirection` will be rejected locally.
      - `triggerPrice`: the price that fires the order.
      - `triggerDirection`: `1` = fire when market price rises to >= `triggerPrice`; `2` = fire when market price falls to <= `triggerPrice`.
    - **Optional**: `triggerBy` is `LastPrice` (fire by last trade price) or `MarkPrice` (fire by mark price). If omitted, the exchange uses its default. Only pass it when the user explicitly asks for a specific trigger price type.
    - Optional `closeOnTrigger=true` makes the triggered order reduce-only (position-closing). Use this when the user says things like "止盈触发后平仓" or "跌到 60000 自动平掉多单".
    - Choose `triggerDirection` by comparing `triggerPrice` with the current market price:
      - Buy when price rises above target → `triggerDirection=1`
      - Sell when price falls below target → `triggerDirection=2`
      - Stop-loss on long (sell when price drops) → `triggerDirection=2`
      - Stop-loss on short (buy when price rises) → `triggerDirection=1`
    - Example: "BTC 涨到 75000 按最新价开多 0.001 张" →
      `perpCreateOrder(symbol='BTCUSDT', side='Buy', positionIdx=1, orderType='Market', qty='0.001', triggerPrice='75000', triggerDirection=1, triggerBy='LastPrice')`
    - Example: "BTC 跌到 65000 按标记价开空 0.001 张" →
      `perpCreateOrder(symbol='BTCUSDT', side='Sell', positionIdx=2, orderType='Market', qty='0.001', triggerPrice='65000', triggerDirection=2, triggerBy='MarkPrice')`
    - Conditional orders show up in `perpGetOpenOrders(orderFilter='StopOrder')`, not in the default `Order` filter.

## Parameter mapping

- BTC / btc → `BTCUSDT`, ETH / eth → `ETHUSDT`, SOL / sol → `SOLUSDT`
- BTC FreeU / btc freeu → `BTCFreeU`, ETH FreeU / eth freeu → `ETHFreeU`
- FreeU 合约余额 → `perpGetBalance(coin='FreeU')`
- 资金账户余额 → `fundGetAssets()`
- 全部钱包总资产 → `getPortfolioNetWorth()`
- 合约资金流水 / 账单流水 → `perpGetWalletFlowRecords(coin='USDT', limit='20', sort='DESC')`
- 合约手续费流水 → `perpGetWalletFlowRecords(coin='USDT', fundType='4', limit='20', sort='DESC')`
- 合约已实现盈亏流水 → `perpGetWalletFlowRecords(coin='USDT', fundType='2', limit='20', sort='DESC')`
- FreeU 持仓 → `perpGetPositions(settleCoin='FreeU')`
- FreeU 挂单 → `perpGetOpenOrders(settleCoin='FreeU')`
- 某个 base coin 的所有挂单（跨 USDT 和 FreeU）→ `perpGetOpenOrders(baseCoin='BTC')`
- 开多 / long / buy → `side=Buy, positionIdx=1`
- 开空 / short / sell → `side=Sell, positionIdx=2`
- 给已有仓位加仓 → 优先 `perpAddToPosition(symbol, positionIdx, qty, pzLinkId?)`
- 平多 → `perpClosePosition(positionIdx=1)`；平空 → `perpClosePosition(positionIdx=2)`；同 symbol 多空一起平 → `perpClosePosition(positionIdx=-1)`（gateway 官方确认 `-1` 表示关所有同 symbol 仓位）
- 市价 → `orderType=Market`, 限价 → `orderType=Limit`
- 止盈限价 → `tpOrderType='Limit'`, `tpLimitPrice='价格'`
- 止损限价 → `slOrderType='Limit'`, `slLimitPrice='价格'`
- 部分止盈止损 → `tpSlMode='Partial'`, `tpSize='数量'`, `slSize='数量'`
- 移动止盈止损 / 追踪止损 / trailing stop → `perpCreateTpSl(symbol, positionIdx, tpSlMode='Full', isMovingTpSl=true, retracePercentage='小数形式回撤', movingTriggerBy?, movingActivationPrice?, retraceDelta?, movingTpSlSize?)`。**retracePercentage 是小数形式**：`'0.005'` = 0.5% 回撤，`'0.01'` = 1%，`'0.02'` = 2%，范围 `[0.001, 1.0)`，**必填**。`movingTriggerBy` 可选（网关默认 `LastPrice`）。`movingActivationPrice` 可选；**传与不传影响状态和可修改性**：不传 → 状态 `Untriggered`（立即生效，**不能**再 `perpReplaceTpSl`）；传了未来价 → 状态 `Unactivated`（等待激活，能 `perpReplaceTpSl`）。两种状态都出现在 `perpGetOpenOrders(orderFilter='StopOrder')`，`stopOrderType='MovingTpSl'`。一个仓位只能挂一个。`retraceDelta` / `movingTpSlSize` 也都透传到 runtime。
- 修改止盈止损 → 先 `perpGetOpenOrders(orderFilter='StopOrder')` 找 `orderId`，再 `perpReplaceTpSl`
- 查当前杠杆 / 保证金模式 → `perpGetModeConfigs(symbol)`，返回 `buyLeverage` / `sellLeverage` / `tradeMode` / `isSeparatePz`。**无仓位也可查**
- 调整 symbol 默认杠杆 → `perpSetLeverage(symbol, buyLeverage)`
- 调整分仓仓位杠杆 → `perpSetLeverage(symbol, buyLeverage, positionIdx=1|2, pzLinkId=<目标仓位>)`
- 切换分仓/合仓 → `perpSwitchPositionMode(coin, isSeparatePz)`，`isSeparatePz=true` 分仓，`false` 合仓。**这是 settle coin 级配置，不是单个 symbol 级配置**；切换 `coin='USDT'` 会影响该结算币下所有 symbol。
- 切换全仓/逐仓 → `perpSwitchMarginMode(symbol, tradeMode, buyLeverage, sellLeverage)`，`tradeMode=0` 全仓，`1` 逐仓
- 调整仓位保证金 → `perpAddMargin(symbol, positionIdx, margin)`；`margin` 为正数 = 加保证金（降低强平价），为负数 = 减保证金（提高强平价，受维持保证金率限制），零值被拒。仅对逐仓仓位生效
- 条件单 → `perpCreateOrder(..., triggerPrice='价格', triggerDirection=1|2, triggerBy='LastPrice')`，`triggerDirection=1` 价格上涨触发 / `2` 价格下跌触发
- 触发后仅减仓 → 追加 `closeOnTrigger=true`
- 资金划转 → `transfer(coin, amount, fromWallet, toWallet)`，钱包类型：`FUNDING` / `TRADING` / `SPOT` / `TRADFI`
  - 划转后必须读回校验：
    - `FUNDING` → `fundGetAssets()`
    - `TRADING` → `perpGetBalance(coin='USDT')`
    - `SPOT` → `spotGetBalance()`
    - `TRADFI` → `tradfiGetBalance()`
- If user says limit order without a price, ask for the price. Do not guess.

## Tools that require symbol or settleCoin

These tools need at least a `symbol` or `settleCoin`. If the user does not specify, ask before calling:
- `perpGetFeeRate` — requires `symbol`
- `perpGetOpenOrders` — pass `symbol` or `settleCoin` or `baseCoin`
- `perpGetOrderHistory`, `perpGetExecutions`, `perpGetClosedPnl` — requires `symbol`

## Known capability gaps

- **TapTrading 账户查询**: 当前已支持资金账户（`fundGetAssets`）、现货账户（`spotGetBalance`）、TradFi 账户（`tradfiGetBalance`）、理财账户（`earnGetBalance`）和合约账户（`perpGetBalance`）查询；TapTrading 账户的持仓/余额查询尚未接入。

## Error handling

- Qty too small: check `getInstruments` for min qty, tell user, then retry.
- Multiple separate positions on close: show all positions with `pzLinkId`, let user choose.
- `perpCreateTpSl` returns success but TP/SL still 0.0: position was not matched (likely missing `pzLinkId`). Re-query and retry with correct `pzLinkId`. Do not tell user "success" until confirmed by `perpGetPositions`.

## Tools available

The following MCP tools are registered under "yubit":

### Read-only (no confirmation needed)
- `getTicker(symbol)` — price, 24h change, volume, funding rate
- `getOrderbook(symbol)` — bid/ask depth
- `getKlines(symbol, interval, limit?, start?, end?)` — last-price candlestick data (OHLCV). `start`/`end` are ms timestamps and must come as a pair.
- `getMarkPriceKlines(symbol, interval, limit?, start?, end?)` — mark-price candlestick data (OHLC only, no volume/turnover). Use when the user explicitly asks about mark-price history. `limit` max 200.
- `getFundingRate(symbol)` — current funding rate
- `getFundingRateHistory(symbol, limit?, startTime?, endTime?)` — historical funding rates, optional ms time range
- `getInstruments(symbol?, status?, limit?, cursor?)` — contract specs (min/max qty, tick size, leverage range, trading status). Omit `symbol` for all; paginate via `limit`/`cursor`.
- `getRiskLimits(symbol?)` — risk-limit tiers per contract (max notional per tier, maintain/initial margin rate, max leverage). Use when user asks about leverage brackets or liquidation thresholds. Omit `symbol` for all.
- `getRecentTrades(symbol)` — recent public trades
- `perpGetBalance(coin?)` — CONTRACT account balance (for perpetual futures). Returns equity, available, position margin, unrealised PnL. NOT the fund/spot/tradfi wallet. Omit coin for all settle coins.
- `perpGetPositions(symbol?, settleCoin?, limit?, cursor?)` — open positions by symbol or settle coin. Must pass at least one of symbol/settleCoin. Supports pagination.
- `perpGetModeConfigs(symbol?, coin?, category?)` — per-symbol position/margin mode configs (`tradeMode`: 0=Cross/1=Isolated, `isSeparatePz`: true=Separate/false=Merged, `buyLeverage`, `sellLeverage`). **Works even without open positions** — use this to check the user's currently configured leverage and mode. Use **before** `perpSwitchMarginMode` / `perpSwitchPositionMode` / `perpSetLeverage`. Omit all args to list the whole account.
- `perpGetFeeRate(symbol)` — maker/taker fee rates
- `perpGetOpenOrders(symbol?, settleCoin?, baseCoin?, orderId?, orderLinkId?, orderFilter?, limit?, cursor?)` — active orders. At least one of symbol/settleCoin/baseCoin must be provided. Pass `orderFilter='StopOrder'` for TP/SL sub-orders. `baseCoin` queries all pairs of a base coin across settle coins (e.g. `baseCoin='BTC'` → `BTCUSDT` + `BTCFreeU`).
- `perpGetOrderHistory(symbol, limit?, orderId?, orderLinkId?, orderStatus?, orderFilter?, cursor?, baseCoin?)` — historical orders with full filter set
- `perpGetExecutions(symbol, limit?, orderId?, execType?, startTime?, endTime?, cursor?, baseCoin?, orderLinkId?, orderFilter?)` — trade executions with time range / filter / pagination
- `perpGetClosedPnl(symbol, limit?, startTime?, endTime?, cursor?)` — closed position PnL with optional time range and pagination
- `perpGetWalletFlowRecords(coin?, startTime?, endTime?, limit?, fundType?, cursor?, sort?, includeFreeU?)` — perp wallet flow / bill records such as transfers, realized PnL, funding fees, and trading fees. `startTime` / `endTime` use Unix seconds, not milliseconds
- `fundGetAssets()` — FUND account asset balances (the central deposit/withdraw/transfer wallet, separate from contract/spot/tradfi accounts). Returns ALL coins with total equity, available balance, frozen amount.
- `getPortfolioNetWorth()` — total balance across ALL wallets (fund + contract + spot + tradfi) in USDT equivalent.
- `getCapabilities()` — machine-readable capability snapshot for the current session.
- `searchTraces(traceId?, orderId?, orderNo?, orderLinkId?, symbol?, toolName?, success?, fromTs?, toTs?, limit?)` — search traces
- `getTrace(traceId)` — get full trace including raw exchange HTTP request/response

### Write
- `perpCreateOrder(symbol, side, orderType, qty, ...)` — place order. Supports conditional/trigger orders via `triggerPrice` + `triggerDirection` + `triggerBy`. `mmp` is optional and only relevant for market-maker accounts.
- `perpAddToPosition(symbol, positionIdx, qty, pzLinkId?)` — safely add to an existing position at market. In separate-position mode it automatically reuses the sole matching `pzLinkId` or rejects when multiple same-direction sub-positions exist and no `pzLinkId` is provided. It post-verifies that no unintended new separate position was opened.
- `perpModifyOrder(symbol, orderId|orderLinkId, ...)` — amend open limit order. Requires at least one field to modify.
- `perpCancelOrder(symbol, orderId|orderLinkId)` — cancel specific order
- `perpCancelAllOrders(symbol?, settleCoin?, confirmBatch?)` — cancel orders. `settleCoin` requires `confirmBatch=true`.
- `perpSetLeverage(symbol, buyLeverage, sellLeverage?, positionIdx?, pzLinkId?)` — set leverage. Without `positionIdx`/`pzLinkId`: sets symbol-wide default. With `positionIdx + pzLinkId`: adjusts a specific separate position's leverage. **Always check `perpGetModeConfigs` first**; if leverage already matches the target, do not submit another write.
- `perpCreateTpSl(symbol, positionIdx, tpSlMode, ...)` — create TP/SL on a position. Supports advanced limit-price TP/SL and trailing stop.
- `perpReplaceTpSl(symbol, orderId, ...)` — modify existing TP/SL sub-order. Find `orderId` via `perpGetOpenOrders(symbol, orderFilter='StopOrder')`.
- `perpSwitchPositionMode(coin, isSeparatePz)` — switch between merged (合仓) and separate (分仓) position mode for a settle coin. **This is coin-level, not symbol-level** — changing `coin='USDT'` affects all symbols under that settle coin. Check current config first and avoid unnecessary writes.
- `perpSwitchMarginMode(symbol, tradeMode, buyLeverage, sellLeverage)` — switch between cross (全仓) and isolated (逐仓) margin mode. Check current config first; if it already matches the target state, do not submit another write.
- `perpAddMargin(symbol, positionIdx, margin, pzLinkId?)` — adjust margin on an isolated position. Positive adds, negative reduces, zero rejected.
- `perpClosePosition(symbol?, settleCoin?, positionIdx?, confirmBatch?)` — close ENTIRE position (no qty, always full close). For partial close, use `perpCreateOrder` with `reduceOnly=true`.
- `transfer(coin, amount, fromWallet, toWallet)` — transfer funds between wallets. Valid wallet types: `FUNDING` (fund account), `TRADING` (contract account), `SPOT` (spot account), `TRADFI` (tradfi account). Returns `requestId`. Follow the transfer notes in Parameter mapping.
