# Prediction Markets

Query templates for prediction market events, markets, traders, and charts.

## Concepts

- **Event**: A container grouping related markets (e.g., "2024 Presidential Election").
- **Market**: An individual binary question within an event (e.g., "Will candidate X win?").
- **Outcome**: Each market has two outcomes (`outcome0`, `outcome1`). `bestAskCT` is the implied probability (0.65 = 65% chance).
- **Collateral Token (CT)**: Prefer CT values over USD for stablecoin-collateral markets since collateral is usually a stablecoin.
- **Trader ID format**: `address:Protocol` (e.g., `0x1234...:Polymarket`).
- **Protocols**: `POLYMARKET`, `KALSHI`.

## 1) Discover prediction market categories

Fetch once and cache. Use `slug` values when filtering events or markets.

```graphql
query PredictionCategories {
  predictionCategories {
    name
    slug
    subcategories {
      name
      slug
      subcategories {
        name
        slug
      }
    }
  }
}
```

## 2) Discover trending events

```graphql
query TrendingEvents {
  filterPredictionEvents(
    filters: { protocol: [POLYMARKET], status: [OPEN] }
    rankings: [{ attribute: trendingScore24h, direction: DESC }]
    limit: 20
  ) {
    count
    page
    results {
      id
      event {
        id
        protocol
        status
        slug
        question
        description
        imageThumbUrl
        venueUrl
        closesAt
        resolvesAt
      }
      status
      markets { id label }
      marketCount
      categories
      trendingScore24h
      relevanceScore24h
      liquidityUsd
      openInterestUsd
      volumeUsd24h
      volumeChange24h
      trades24h
      uniqueTraders24h
    }
  }
}
```

Filter by category with `categories: ["sports"]`. Search by keyword with `phrase: "election"`.

Scoring metrics:
- `trendingScore24h`: Volume + trades + momentum — "what's hot right now"
- `relevanceScore24h`: Factors in liquidity and market maturity — "most important"
- `competitiveScore24h`: Markets only (not events), measures outcome closeness
- All available at 5m, 1h, 4h, 12h, 24h, and 1w windows

## 3) Discover individual markets

```graphql
query CompetitiveMarkets {
  filterPredictionMarkets(
    filters: { status: [OPEN] }
    rankings: [{ attribute: competitiveScore24h, direction: DESC }]
    limit: 20
  ) {
    count
    results {
      id
      eventLabel
      market {
        id
        eventId
        protocol
        label
        question
        imageThumbUrl
        status
        closesAt
      }
      status
      outcome0 {
        label
        bestAskCT
        bestBidCT
        spreadCT
        lastPriceCT
        liquidityCT
        volumeUsd24h
        priceChange24h
      }
      outcome1 {
        label
        bestAskCT
        bestBidCT
        spreadCT
        lastPriceCT
        liquidityCT
        volumeUsd24h
        priceChange24h
      }
      competitiveScore24h
      trendingScore24h
      liquidityUsd
      openInterestUsd
      volumeUsd24h
      trades24h
      priceCompetitiveness
    }
  }
}
```

Markets within an event, ranked by probability:

```graphql
query EventMarkets {
  filterPredictionMarkets(
    eventIds: ["yourEventId"]
    rankings: [{ outcome: outcome0, outcomeAttribute: bestAskCT, direction: DESC }]
    limit: 50
  ) {
    count
    results {
      id
      market { id label question }
      outcome0 {
        label
        bestAskCT
        bestBidCT
        lastPriceCT
        volumeUsd24h
      }
      outcome1 {
        label
        bestAskCT
        bestBidCT
        lastPriceCT
        volumeUsd24h
      }
      volumeUsdAll
      liquidityUsd
      openInterestUsd
    }
  }
}
```

High open-interest markets closing soon:

```graphql
query ClosingSoon {
  filterPredictionMarkets(
    filters: {
      status: [OPEN]
      closesAt: { lte: 1773700000 }
    }
    rankings: [{ attribute: openInterestUsd, direction: DESC }]
    limit: 20
  ) {
    count
    results {
      id
      market { id label question closesAt resolvesAt }
      outcome0 { label bestAskCT lastPriceCT }
      outcome1 { label bestAskCT lastPriceCT }
      openInterestUsd
      liquidityUsd
      volumeUsd24h
    }
  }
}
```

Sort dropdown mappings:
- "Trending" → `trendingScore24h` DESC
- "Most Volume" → `volumeUsd24h` DESC
- "Most Liquidity" → `liquidityUsd` DESC
- "Newest" → `age` ASC
- "Closing Soon" → `closesAt` ASC (with status OPEN filter)
- "Most Competitive" → `competitiveScore24h` DESC (markets only)

## 4) Detailed event stats (event detail page)

```graphql
query DetailedPredictionEventStats {
  detailedPredictionEventStats(input: { eventId: "yourEventId" }) {
    eventId
    lastTransactionAt
    predictionEvent {
      id
      protocol
      venueEventId
      status
      question
      url
      rulesPrimary
      rulesSecondary
      tags
      opensAt
      closesAt
      resolvesAt
      resolvedAt
      resolution { result source }
      imageLargeUrl
      imageThumbUrl
      createdAt
      updatedAt
      networkId
      marketIds
      categories { name slug subcategories { name slug } }
    }
    predictionMarkets {
      id
      protocol
      venueMarketId
      eventId
      question
      label
      eventLabel
      outcomeLabels
      outcomeIds
      resolution { result source }
      imageThumbUrl
      createdAt
      opensAt
      closesAt
      resolvesAt
      resolvedAt
      networkId
    }
    statsDay1 {
      start
      end
      statsCurrency {
        volumeUsd
        volumeCT
        openLiquidityUsd
        closeLiquidityUsd
        openOpenInterestUsd
        closeOpenInterestUsd
      }
      statsNonCurrency { trades uniqueTraders }
      statsChange { volumeChange openLiquidityChange openOpenInterestChange tradesChange uniqueTradersChange }
      scores { trending relevance }
    }
    allTimeStats { volumeUsd volumeCT venueVolumeUsd venueVolumeCT }
    lifecycle { ageSeconds expectedLifespanSeconds timeToResolutionSeconds isResolved }
  }
}
```

## 5) Single market OHLC chart

Supported resolutions: `min1`, `min5`, `min15`, `min30`, `hour1`, `hour4`, `hour12`, `day1`, `week1`.

```graphql
query PredictionMarketBars {
  predictionMarketBars(input: {
    marketId: "yourMarketId"
    from: 1773100000
    to: 1773700000
    resolution: hour1
  }) {
    marketId
    predictionMarket {
      id
      label
      question
      outcomeLabels
      eventLabel
    }
    bars {
      t
      volumeUsd
      volumeCollateralToken
      trades
      uniqueTraders
      openInterestUsd { o h l c }
      outcome0 {
        trades
        buys
        sells
        volumeUsd
        buyVolumeUsd
        sellVolumeUsd
        priceUsd { o h l c }
        priceCollateralToken { o h l c }
        liquidityCollateralToken { o h l c }
        bidCollateralToken { o h l c }
        askCollateralToken { o h l c }
      }
      outcome1 {
        trades
        buys
        sells
        volumeUsd
        buyVolumeUsd
        sellVolumeUsd
        priceUsd { o h l c }
        priceCollateralToken { o h l c }
        liquidityCollateralToken { o h l c }
        bidCollateralToken { o h l c }
        askCollateralToken { o h l c }
      }
    }
  }
}
```

Additional parameters: `countback` (last N bars from `to`), `removeEmptyBars` (skip inactive bars).

## 6) Multi-market probability comparison chart

Returns up to 10 markets' OHLC bars in one request. Plot `outcome0.priceCollateralToken.c` for each market as separate colored lines.

```graphql
query TopMarketsByVolume {
  predictionEventTopMarketsBars(input: {
    eventId: "yourEventId"
    from: 1773100000
    to: 1773700000
    resolution: hour1
    limit: 5
    rankBy: volumeUsd1w
    rankDirection: DESC
  }) {
    eventId
    predictionEvent { id question }
    marketBars {
      marketId
      predictionMarket {
        id
        label
        outcomeLabels
      }
      bars {
        t
        outcome0 {
          priceCollateralToken { o h l c }
          volumeUsd
          trades
        }
        outcome1 {
          priceCollateralToken { o h l c }
        }
        openInterestUsd { o h l c }
        volumeUsd
      }
    }
  }
}
```

Ranking options: `rankBy` for market attributes, or `rankByOutcome` + `rankByOutcomeAttribute` for outcome-level sorting. The `marketIds` parameter overrides ranking.

## 7) Event-level aggregated chart

Does not include per-outcome price data. Use for volume, liquidity, and open interest charts.

```graphql
query PredictionEventBars {
  predictionEventBars(input: {
    eventId: "yourEventId"
    from: 1773100000
    to: 1773700000
    resolution: day1
  }) {
    eventId
    predictionEvent { id question marketIds }
    bars {
      t
      volumeUsd
      buyVolumeUsd
      sellVolumeUsd
      totalVolumeUsd
      trades
      uniqueTraders
      liquidityUsd { o h l c }
      openInterestUsd { o h l c }
    }
  }
}
```

## 8) Recent trades for an event

```graphql
query EventTrades {
  predictionTrades(input: { eventId: "yourEventId", limit: 50 }) {
    items {
      marketId
      outcomeId
      protocol
      tradeType
      maker
      traderId
      timestamp
      outcomeIndex
      outcomeLabel
      priceUsd
      priceCollateral
      amount
      amountUsd
      transactionHash
      networkId
    }
    cursor
  }
}
```

## 9) Outcome token holders

```graphql
query TokenHolders {
  predictionTokenHolders(input: {
    marketId: "yourMarketId"
    tokenId: "yourTokenId"
    limit: 25
  }) {
    items {
      walletAddress
      amount
      predictionTrader { alias }
    }
    total
    cursor
  }
}
```

## 10) Trader leaderboard

```graphql
query TopTraders {
  filterPredictionTraders(
    rankings: [{ attribute: TOTAL_PROFIT_CT_ALL, direction: DESC }]
    limit: 25
  ) {
    count
    page
    results {
      id
      trader {
        id
        venueTraderId
        protocol
        alias
        primaryAddress
        profileImageUrl
        profileUrl
        labels
      }
      totalVolumeUsdAll
      totalProfitUsdAll
      totalProfitCTAll
      totalTradesAll
      activeMarketsCount
      pnlPerVolumeAll
      biggestWinUsd
      biggestLossUsd
      firstTradeTimestamp
      lastTradeTimestamp
      volumeUsd24h
      realizedPnlUsd24h
      realizedProfitPercentage24h
      trades24h
      winRate24h
      heldTokenAcquisitionCostUsd
    }
  }
}
```

Ranking attributes available at 12h, 24h, 1w, 1m, and "All" (all-time) windows. Use volume filters (e.g., `totalVolumeUsdAll: { gte: 10000 }`) for meaningful leaderboards. `pnlPerVolumeAll` normalizes profit by capital deployed.

Other leaderboard variants:
- Best win rate: rank by `WIN_RATE_1W` DESC with volume floor filter
- Highest 24h PnL: rank by `REALIZED_PNL_USD_24H` DESC
- Search by alias/address: use `phrase` parameter

## 11) Trader profile and detailed stats

```graphql
query TraderProfile {
  detailedPredictionTraderStats(input: {
    traderId: "0x02227b8f5a9636e895607edd3185ed6ee5598ff7:Polymarket"
  }) {
    traderId
    lastTransactionAt
    trader {
      id
      protocol
      venueTraderId
      alias
      primaryAddress
      linkedAddresses
      profileImageUrl
      profileUrl
      labels
      totalVolumeUsd
      totalVolumeCT
      allTimeProfitUsd
      allTimeProfitCT
      biggestWinUsd
      biggestWinCT
      biggestLossUsd
      biggestLossCT
      totalTradesCount
      activeMarketsCount
      firstTradeTimestamp
      lastTradeTimestamp
    }
    allTimeStats {
      totalVolumeUsd
      totalVolumeCT
      totalProfitUsd
      totalProfitCT
    }
    statsDay1 {
      start
      end
      lastTransactionAt
      statsCurrency {
        volumeUsd
        volumeCT
        buyVolumeUsd
        sellVolumeUsd
        realizedPnlUsd
        realizedPnlCT
        averageSwapAmountUsd
        averageProfitUsdPerTrade
        realizedProfitPercentage
        heldTokenAcquisitionCostUsd
        soldTokenAcquisitionCostUsd
      }
      statsNonCurrency {
        trades
        buys
        sells
        wins
        losses
        uniqueMarkets
      }
      statsChange {
        volumeChange
        realizedPnlChange
        tradesChange
        winsChange
        lossesChange
        uniqueMarketsChange
      }
    }
  }
}
```

Windowed stats available: `statsHour1` through `statsDay30`.

## 12) Trader market positions

Open positions sorted by volume:

```graphql
query OpenPositions {
  filterPredictionTraderMarkets(
    traderIds: ["0x02227b8f5a9636e895607edd3185ed6ee5598ff7:Polymarket"]
    filters: { hasOpenPosition: true }
    rankings: [{ attribute: totalVolumeUsd, direction: DESC }]
    limit: 25
  ) {
    count
    results {
      id
      traderId
      marketId
      eventId
      market {
        id
        eventId
        label
        question
        eventLabel
        imageThumbUrl
        outcome0Label
        outcome1Label
      }
      hasOpenPosition
      totalRealizedPnlUsd
      totalRealizedPnlCT
      totalVolumeUsd
      totalTrades
      totalCostBasisUsd
      totalSharesHeld
      pnlPerVolumeMarket
      outcome0 {
        outcomeId
        isWinningOutcome
        sharesHeld
        avgEntryPriceUsd
        avgEntryPriceCT
        costBasisUsd
        buys
        sells
        buyVolumeUsd
        sellVolumeUsd
        realizedPnlUsd
        pnlStatus
      }
      outcome1 {
        outcomeId
        isWinningOutcome
        sharesHeld
        avgEntryPriceCT
        costBasisUsd
        buys
        sells
        realizedPnlUsd
        pnlStatus
      }
    }
  }
}
```

`filterPredictionTraderMarkets` works bidirectionally — filter by `traderIds` for a portfolio view, or by `marketIds`/`eventIds` for top traders in a market/event.

## 13) Trader performance chart

Plot `cumulativeRealizedPnlCT` for the signature trader P&L curve.

```graphql
query TraderPerformance {
  predictionTraderBars(input: {
    traderId: "0x02227b8f5a9636e895607edd3185ed6ee5598ff7:Polymarket"
    from: 1773100000
    to: 1773700000
    resolution: day1
  }) {
    traderId
    trader {
      id
      alias
      primaryAddress
      profileImageUrl
    }
    bars {
      t
      trades
      buys
      sells
      uniqueMarkets
      volumeUsd
      volumeCT
      buyVolumeUsd
      sellVolumeUsd
      wins
      losses
      realizedPnlUsd
      realizedPnlCT
      cumulativeRealizedPnlUsd
      cumulativeRealizedPnlCT
    }
  }
}
```

## 14) Trader trade history

```graphql
query TraderTrades {
  predictionTrades(input: {
    traderId: "0x02227b8f5a9636e895607edd3185ed6ee5598ff7:Polymarket"
    limit: 50
  }) {
    items {
      marketId
      outcomeId
      protocol
      tradeType
      maker
      traderId
      timestamp
      outcomeIndex
      outcomeLabel
      priceUsd
      priceCollateral
      amount
      amountCollateral
      amountUsd
      transactionHash
      blockNumber
      networkId
      predictionMarket {
        id
        label
        question
        eventLabel
        outcomeLabels
      }
    }
    cursor
  }
}
```

## Resolution selection guide

| Time Range | Recommended Resolution |
| --- | --- |
| Last hour | min1 |
| Last 4 hours | min5 |
| Last 24 hours | min15 or min30 |
| Last week | hour1 |
| Last month | hour4 or hour12 |
| Last 3 months | day1 |
| All time | day1 or week1 |

## Recommended page data flows

**Event detail page** (run 1–4 in parallel on load):
1. `detailedPredictionEventStats` — metadata, markets, stats
2. `filterPredictionMarkets(eventIds)` — current outcome pricing
3. `predictionEventTopMarketsBars` — multi-market probability chart
4. `predictionEventBars` — volume/liquidity/OI chart
5. `predictionTrades(eventId)` — recent trades
6. `predictionMarketBars` — drill-down on market select
7. `predictionTokenHolders` — on token holder tab

**Trader profile page** (run 1–3 in parallel on load):
1. `detailedPredictionTraderStats` — profile header and summary stats
2. `filterPredictionTraderMarkets(traderIds, hasOpenPosition: true)` — active positions
3. `predictionTraderBars` — cumulative P&L chart
4. `filterPredictionTraderMarkets(traderIds)` — all positions (on tab switch)
5. `predictionTrades(traderId)` — trade history (on tab switch)
