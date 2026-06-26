# Codex Supergraph Endpoint Playbook

Use this map to pick the best operation quickly.

## Discovery and search

| Intent | Preferred query | Notes |
| --- | --- | --- |
| Discover tradable tokens with ranking/filtering | `filterTokens` | Supports phrase search and quality filters; response limit 200. |
| Trending tokens | `filterTokens` | Rank by `trendingScore24` DESC with `statsType: "FILTERED"`. Use `trendingIgnored: false` and `potentialScam: false` filters to exclude noise. |
| Find pairs for a token | `listPairsWithMetadataForToken` | Useful before charting or pair-specific metadata. |
| Find wallet leaders for a token | `filterTokenWallets` | Good for holder quality and top-wallet analysis. |

## Pricing and charts

| Intent | Preferred query | Preferred subscription | Notes |
| --- | --- | --- | --- |
| Get fast current or historical token price snapshots | `getTokenPrices` | `onPriceUpdated` (single token) | Uses aggregate weighted prices unless source pair is provided. |
| Stream prices for many tokens | N/A | `onPricesUpdated` | Batch token inputs in one subscription; start around 25 tokens. |
| Build pair chart candles | `getBars` | `onBarsUpdated` | `getBars` max datapoints is 1500 per request. |
| Build aggregate token chart candles | `getTokenBars` | `onTokenBarsUpdated` | Aggregates across top liquidity pairs. `onTokenBarsUpdated` returns per-resolution `aggregates`, not a flat `bars` array. |
| Fetch pair metrics and stat windows | `pairMetadata` | `onPairMetadataUpdated` | Use query for initial load, subscription for live refresh. |
| Windowed token change stats (period-over-period) | `getDetailedTokenStats` | N/A | Per-window deltas (`stats_min5`…`stats_day1`) as `{ previousValue, currentValue, change }`. Complements `filterTokens` on a detail page. |

## Events and flows

| Intent | Preferred query | Preferred subscription | Notes |
| --- | --- | --- | --- |
| Fetch token transactions | `getTokenEvents` | `onTokenEventsCreated` | Choose subscription for live feeds. |
| Fetch maker-specific activity | `getTokenEventsForMaker` | `onEventsCreatedByMaker` | Use maker address filters. |
| Track unconfirmed Solana events | N/A | `onUnconfirmedEventsCreated` | Solana-focused unconfirmed flow. |

## Wallet analytics

| Intent | Preferred query | Notes |
| --- | --- | --- |
| Wallet-level chart and performance data | `walletChart`, `detailedWalletStats` | Use date windows and aggregation granularity intentionally. |
| Holder distribution | `holders`, `top10HoldersPercent` | Combine with token metadata for context. |

## Launchpads and high-throughput streams

| Intent | Preferred subscription | Notes |
| --- | --- | --- |
| Launchpad token event firehose | `onLaunchpadTokenEventBatch` | High-frequency stream; isolate connection and proxy through backend. |
| Per-event launchpad updates | `onLaunchpadTokenEvent` | Use when batch handling is not needed. |

## Prediction markets

| Intent | Preferred query | Notes |
| --- | --- | --- |
| Discover trending prediction events | `filterPredictionEvents` | Rank by `trendingScore24h`, `relevanceScore24h`, or `volumeUsd24h`. Filter by `protocol`, `status`, `categories`. |
| Search prediction events by keyword | `filterPredictionEvents` | Use `phrase` parameter. |
| Discover/filter individual markets | `filterPredictionMarkets` | Rank by `competitiveScore24h`, outcome attributes, or `openInterestUsd`. Filter by `eventIds`, `status`, `closesAt`. |
| Prediction event detail page | `detailedPredictionEventStats` | Full metadata, markets list, windowed stats, lifecycle. |
| Event market pricing | `filterPredictionMarkets` | Filter by `eventIds`, rank by `outcome0.bestAskCT` for probability sort. |
| Single market OHLC chart | `predictionMarketBars` | Per-outcome price, bid/ask, volume, OI. Resolutions: min1 through week1. |
| Multi-market probability comparison | `predictionEventTopMarketsBars` | Up to 10 markets in one request. Plot `outcome0.priceCollateralToken.c` per market. |
| Event volume/liquidity/OI chart | `predictionEventBars` | Aggregated across all markets in the event. No per-outcome price data. |
| Prediction trades | `predictionTrades` | Filter by `eventId`, `marketId`, or `traderId`. Cursor-paginated. |
| Outcome token holders | `predictionTokenHolders` | Requires `marketId` and `tokenId`. |
| Prediction categories | `predictionCategories` | Fetch once and cache. Use `slug` for filtering. |
| Trader leaderboard | `filterPredictionTraders` | Rank by profit, win rate, PnL. Filter by volume floors. Search by `phrase`. |
| Trader profile and stats | `detailedPredictionTraderStats` | All-time and windowed stats (statsHour1 through statsDay30). |
| Trader positions | `filterPredictionTraderMarkets` | Bidirectional: by `traderIds` for portfolio, by `marketIds`/`eventIds` for top traders. |
| Trader performance chart | `predictionTraderBars` | Plot `cumulativeRealizedPnlCT` for P&L curve. |

## Auth and token management

| Intent | Preferred mutation/query | Notes |
| --- | --- | --- |
| Create short-lived API tokens | `createApiTokens` | Use long-lived key for creation. |
| List existing API tokens | `apiTokens` | Not available with short-lived keys. |
| Revoke API token | `deleteApiToken` | Use server-side secret key context. |

## Webhooks

Server-side push alerts (HTTP POST to a `callbackUrl`) for backend/serverless alerting. See template #24.

| Intent | Preferred mutation/query | Notes |
| --- | --- | --- |
| Create event webhooks | `createWebhooks` | One wrapper input; pick a family: `tokenPriceEventWebhooksInput`, `marketCapWebhooksInput`, `tokenTransferEventWebhooksInput`, `tokenPairEventWebhooksInput`, `predictionTradeWebhooksInput`, `predictionMarketMetricsEventWebhooksInput`. Long-lived key only. |
| Delete webhooks | `deleteWebhooks` | Pass `{ webhookIds: [...] }`. |
| List webhooks | `getWebhooks` | Cursor-paginated; filter subgroups by `bucketKey`. |

Webhook vs subscription: use a **subscription** when a live client (browser/app) is connected and you want push updates into a UI; use a **webhook** when there's no persistent connection — a backend or serverless function that should be called when a price/cap/transfer condition fires. Webhooks survive restarts and don't require holding a socket open. Note: the MPP 402 (codex-gateway) flow is query-only, so neither subscriptions nor webhooks are available there — `createWebhooks` / `deleteWebhooks` are mutations and need API key auth.

## Recommended page data flows

Named page-flows for the token side, mirroring the prediction page-flows in [prediction-markets.md](prediction-markets.md). Compose the templates in [query-templates.md](query-templates.md).

**Detailed token page** (run the load group in parallel):
1. `filterTokens` (`tokens: ["tokenAddress:networkId"]`) — primary header call; carries most of the data in one request: `priceUSD`, `marketCap`, `circulatingMarketCap`, `liquidity`, `volume24`, `buyVolume24`, `sellVolume24`, `txnCount24`, `holders`, plus `top10HoldersPercent`, `isScam`, `potentialScamReasons` (concentration and safety on the same response).
2. `getDetailedTokenStats` (`networkId`, `tokenAddress`, `statsType: FILTERED`) — windowed period-over-period change stats `filterTokens` does not return (template #17).
3. `getTokenBars` (`symbol: "tokenAddress:networkId"`) — price chart. Default to `getTokenBars` (token aggregate across pairs) unless you want a pair-specific chart, then use `getBars` with `pairAddress:networkId`. Defaults: 15-minute resolution, `countback` up to 1500 (max), `removeLeadingNullValues: true`.
4. `holders` (`input: HoldersInput`) — holder list in `items` (`address`, `balance`, `shiftedBalance`, `balanceUsd`) with `count`; `top10HoldersPercent` and `status` come back on the same call.
5. `getTokenEvents` (`query: { address, networkId }`) — recent trades; `address` auto-resolves to the top pair; cursor-paginated, `direction: DESC` default.
6. `token` (`input: TokenInput`) — static metadata (parallel or follow-on): `name`, `symbol`, `socialLinks`, `info`, `creatorAddress`, and (Solana) mint/freeze-authority validity flags.
7. `filterTokenWallets` (`input: { tokenIds: ["tokenAddress:networkId"] }`) — top-wallet table on the holders tab; rank by `realizedProfitUsd1d` for a smart-money view. (`tokenIds` is current; `tokenId` is deprecated.)
8. `getTokenEventsForMaker` (`query: { maker, networkId, tokenAddress }`) — single-wallet drill-down on maker-row click.

Real-time layer (attach after initial hydration):
- `onPriceUpdated` (`address`, `networkId`) — live header price. Prefer this single subscription over batch `onPricesUpdated` when one token is on screen.
- `onTokenEventsCreated` (template #19) — live trade feed appended to step 5.
- `onTokenBarsUpdated` (template #21) — live candle updates for the step-3 chart.

Safety / concentration: read `top10HoldersPercent`, `isScam`, and `potentialScamReasons` (`MinimumLiquidity`, `LiquidityRugPull`, `SuspiciousWalletActivity`, `AbnormalBuyerRatio`) straight off the step-1 result — no dedicated calls needed.

**Charts.** Default to `getTokenBars` (token-level aggregate across pairs); use `getBars` only when a pair-specific chart is wanted. Defaults: 15-minute resolution, `countback` up to 1500 (max), `removeLeadingNullValues: true`. Attach `onTokenBarsUpdated` (template #21) for live candles — note its response is per-resolution `aggregates`, not a flat `bars` array.

**Events.** For a token: `getTokenEvents` for history, then `onTokenEventsCreated` (template #19) for the live feed. For a wallet: `getTokenEventsForMaker` for history, then `onEventsCreatedByMaker` (template #20) for the live feed. The live maker subscription takes only `makerAddress` (no network/token filter), unlike the query.

**Wallets.** `filterTokenWallets` to rank traders for a token (rank by `realizedProfitUsd1d` for smart money), then `detailedWalletStats` (template #18) for a single wallet's full profile, and `walletChart` (template #15) for its history. Reading quality: `scammerScore` / `botScore` and `labels` for trust, `realizedProfitUsd` plus `wins` / `losses` for performance, `avgHoldPeriodSec` for style.

**Launchpad lifecycle.** Stream `onLaunchpadTokenEvent` or the batch variant (template #22), filtered by `eventType`, to follow a token through its lifecycle: `Deployed` is the earliest, fastest signal for brand-new tokens, but metadata (name, symbol, image) may not be populated yet — it becomes available at `Created`. Then `Updated` during trading, `Completed` when it graduates off the bonding curve, and `Migrated`. Remember the payload is a token snapshot (market cap, holder-quality percentages, fees), not a transaction.

## Selection heuristics

- Prefer one-shot queries for initial page hydration.
- Add subscriptions only where visible realtime UX exists.
- Choose aggregated endpoints when user intent is token-level, not pool-level.
- Keep fields minimal for first pass; expand only after payload shape is verified.
