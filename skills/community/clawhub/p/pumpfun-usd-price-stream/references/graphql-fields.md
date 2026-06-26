# Bitquery Trading.Tokens — PumpFun GraphQL Field Reference

Full reference for the fields available in the `Trading.Tokens` **subscription** on the Bitquery streaming API, scoped to PumpFun tokens on Solana. For real-time streaming, use a `subscription` with the same structure (no `limit`/`orderBy`).

## Subscription Structure

```graphql
subscription {
  Trading {
    Tokens(
      where: <FilterInput>
    ) {
      Token { ... }
      Block { ... }
      Interval { ... }
      Volume { ... }
      Price { ... }
    }
  }
}
```

---

## Filters (`where`) for PumpFun

### Token / Network Filters

| Filter | Description | Example |
|--------|-------------|---------|
| `Token.Network.is` | Match a specific blockchain network | `"Solana"` |
| `Token.Address.includesCaseInsensitive` | Match tokens whose address includes the string | `"pump"` |
| `Token.Address.is` | Match a specific token contract address exactly | `"AbcDef...pumpXyz"` |
| `Token.Symbol.is` | Match by ticker symbol | `"BONK"` |
| `Token.NetworkBid` | Bitquery network bid filter (required for PumpFun queries) | `{}` |

**PumpFun filter (the active subscription filter):**
```graphql
where: {
  Interval: {Time: {Duration: {eq: 1}}},
  Token: {
    NetworkBid: {},
    Network: {is: "Solana"},
    Address: {includesCaseInsensitive: "pump"}
  }
}
```

### Time / Interval Filters

| Filter | Description | Example |
|--------|-------------|---------|
| `Interval.Time.Duration.eq` | Candle duration in seconds: 1 = 1 second tick; 5, 60, 1440 = minutes | `1`, `5`, `60`, `1440` |
| `Block.Time.after` | Filter data after this ISO timestamp | `"2025-01-01T00:00:00Z"` |
| `Block.Time.before` | Filter data before this ISO timestamp | `"2025-12-31T23:59:59Z"` |
| `Block.Time.between` | Array of [start, end] ISO timestamps | `["2025-01-01", "2025-02-01"]` |

---

## Output Fields

### `Token`

| Field | Type | Description |
|-------|------|-------------|
| `Address` | String | Token contract address on Solana (the pump.fun token mint address) |
| `Id` | String | Bitquery token ID |
| `IsNative` | Boolean | True if native coin (usually false for PumpFun tokens) |
| `Name` | String | Token full name |
| `Network` | String | Blockchain network (always `Solana` for PumpFun) |
| `Symbol` | String | Ticker symbol (e.g., `BONK`, `WIF`, etc.) |
| `TokenId` | String | Internal Bitquery token ID |

### `Block`

| Field | Type | Description |
|-------|------|-------------|
| `Date` | String | Date in `YYYY-MM-DD` format |
| `Time` | String | ISO timestamp of the block |
| `Timestamp` | Integer | Unix timestamp |

### `Interval`

| Field | Type | Description |
|-------|------|-------------|
| `Time.Start` | String | Interval start ISO timestamp |
| `Time.End` | String | Interval end ISO timestamp |
| `Time.Duration` | Integer | Interval duration: 1 = 1 second tick; other values in minutes |

### `Volume`

| Field | Type | Description |
|-------|------|-------------|
| `Base` | Float | Volume in the base token |
| `Quote` | Float | Volume in the quote token |
| `Usd` | Float | Volume in USD |

### `Price`

| Field | Type | Description |
|-------|------|-------------|
| `IsQuotedInUsd` | Boolean | Whether price is quoted in USD |
| `Ohlc.Open` | Float | Opening price |
| `Ohlc.High` | Float | Highest price in the interval |
| `Ohlc.Low` | Float | Lowest price in the interval |
| `Ohlc.Close` | Float | Closing price |
| `Average.Mean` | Float | Simple arithmetic mean price |
| `Average.SimpleMoving` | Float | Simple moving average |
| `Average.ExponentialMoving` | Float | Exponential moving average |
| `Average.WeightedSimpleMoving` | Float | Weighted simple moving average |

---

## Example: Filter a Specific PumpFun Token by Address

```graphql
subscription {
  Trading {
    Tokens(
      where: {
        Interval: {Time: {Duration: {eq: 1}}},
        Token: {
          NetworkBid: {},
          Network: {is: "Solana"},
          Address: {is: "YourSpecificPumpFunTokenAddressHere"}
        }
      }
    ) {
      Token { Address Name Symbol }
      Block { Time }
      Price { Ohlc { Open High Low Close } }
      Volume { Usd }
    }
  }
}
```

## Example: 5-Minute Candles for PumpFun Tokens

```graphql
subscription {
  Trading {
    Tokens(
      where: {
        Interval: {Time: {Duration: {eq: 5}}},
        Token: {
          NetworkBid: {},
          Network: {is: "Solana"},
          Address: {includesCaseInsensitive: "pump"}
        }
      }
    ) {
      Token { Address Name Symbol }
      Block { Time }
      Price { Ohlc { Open High Low Close } Average { SimpleMoving ExponentialMoving } }
      Volume { Usd }
    }
  }
}
```

## Example: Full Subscription (all fields)

```graphql
subscription {
  Trading {
    Tokens(
      where: {
        Interval: {Time: {Duration: {eq: 1}}},
        Token: {
          NetworkBid: {},
          Network: {is: "Solana"},
          Address: {includesCaseInsensitive: "pump"}
        }
      }
    ) {
      Token {
        Address
        Id
        IsNative
        Name
        Network
        Symbol
        TokenId
      }
      Block {
        Date
        Time
        Timestamp
      }
      Interval {
        Time {
          Start
          Duration
          End
        }
      }
      Volume {
        Base
        Quote
        Usd
      }
      Price {
        IsQuotedInUsd
        Ohlc {
          Close
          High
          Low
          Open
        }
        Average {
          ExponentialMoving
          Mean
          SimpleMoving
          WeightedSimpleMoving
        }
      }
    }
  }
}
```

---

## Notes on PumpFun Token Prices

- PumpFun tokens are Solana SPL tokens with very small USD prices (often `< $0.000001`)
- Use 6–8 decimal places when formatting prices (avoid `$0.00` display)
- Volume in USD can vary widely from nearly zero to millions depending on token activity
- Tokens may appear/disappear in the stream as trading activity starts/stops
