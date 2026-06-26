# Codex Supergraph API Reference

## Endpoint model

- HTTP GraphQL: `https://graph.codex.io/graphql`
- WebSocket GraphQL: `wss://graph.codex.io/graphql`

## Auth matrix

| Mode | Headers | Supports | Notes |
| ---- | ------- | -------- | ----- |
| API key | `Authorization: <key>` | query, mutation, subscription | Standard path |
| Short-lived token | `Authorization: Bearer <token>` | query, mutation, subscription | Token-scoped limits |

## Common network IDs

| Network | `networkId` |
| ------- | ----------- |
| Ethereum | `1` |
| Base | `8453` |
| Arbitrum | `42161` |
| Polygon | `137` |
| Tempo | `4217` |
| Optimism | `10` |
| BNB Chain | `56` |
| Avalanche | `43114` |
| Solana | `1399811149` |

Run `getNetworks` once per session for the full list.

## Session preflight

```graphql
query GetNetworks {
  getNetworks {
    id
    name
  }
}
```

Use to validate `networkId` before price/event/chart requests.

## Operation matrix

| Task | Operation | Type | Notes |
| ---- | --------- | ---- | ----- |
| Network list | `getNetworks` | Query | Run once per session |
| Discover/search tokens | `filterTokens` | Query | Recommended first step |
| Snapshot token prices | `getTokenPrices` | Query | Weighted price output |
| Pair metadata/stats | `pairMetadata` | Query | Pair id: `pairAddress:networkId` |
| Pair bars (OHLCV) | `getBars` | Query | Keep datapoints bounded |
| Token bars | `getTokenBars` | Query | Aggregate bars |
| Token events | `getTokenEvents` | Query | Historical stream |
| Maker events | `getTokenEventsForMaker` | Query | Wallet scoped |
| Holders | `holders` | Query | Distribution views |
| Top holder concentration | `top10HoldersPercent` | Query | Concentration metric |
| Live token price | `onPriceUpdated` | Subscription | Single token |
| Live token prices | `onPricesUpdated` | Subscription | Multi token batch |
| Live pair stats | `onPairMetadataUpdated` | Subscription | Pair updates |
| Live bars | `onBarsUpdated`, `onTokenBarsUpdated` | Subscription | Chart updates |
| Create short-lived tokens | `createApiTokens` | Mutation | Needs long-lived key |
| Manage short-lived tokens | `apiTokens`, `apiToken`, `deleteApiToken` | Query/Mutation | Not available from short-lived token |

## WebSocket constraints

- Protocol: `graphql-transport-ws`
- Send `connection_init` with `Authorization` in payload
- Wait for `connection_ack`
- Unsubscribe with `complete`

## Common failures

| Symptom | Likely cause | Fix |
| ------- | ------------ | --- |
| 401 / UNAUTHENTICATED | Missing or invalid API auth | Validate key/token and header format |
| 429 / Too Many Requests | Rate limit exceeded | Back off with exponential delay and retry |
| GraphQL validation error | Input shape mismatch | Check operation args and variable types |

See [gotchas.md](gotchas.md) for detailed failure patterns (symbol formats, pagination, rate limits, etc.).
