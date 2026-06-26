# Trade It Enums and Constants

Use these values exactly. Do not invent alternates.

## Brokerage ids

```json
{
  "BrokerageID": {
    "Robinhood": 1,
    "ETrade": 2,
    "Coinbase": 3,
    "Kraken": 5,
    "CharlesSchwab": 7,
    "Webull": 8,
    "Public": 11,
    "Tastytrade": 12
  }
}
```

## Brokerage token status

```json
{
  "BrokerageTokenStatus": {
    "Pending": 0,
    "Verified": 1,
    "Error": 10
  }
}
```

Use `Verified` before attempting account reads or trade placement.

## Trade action

```json
{
  "TradeAction": {
    "Buy": "buy",
    "Sell": "sell"
  }
}
```

Use `buy` to open or add long exposure, and `sell` to reduce or close supported positions.

## Position effect

```json
{
  "PositionEffect": {
    "Open": "open",
    "Close": "close"
  }
}
```

Use `open` when initiating a position and `close` when reducing or exiting an existing position.

## Order type

```json
{
  "OrderType": {
    "Market": "market",
    "Limit": "limit",
    "Stop": "stop",
    "StopLimit": "stop_limit"
  }
}
```

`market` executes at prevailing price, `limit` executes at your limit price or better, and stop variants trigger from stop conditions.

## Order direction

```json
{
  "OrderDirection": {
    "Debit": "debit",
    "Credit": "credit"
  }
}
```

For options, `debit` means paying premium; `credit` means receiving premium.

## Time in force

```json
{
  "TimeInForce": {
    "Day": "day",
    "GoodTillCanceled": "gtc",
    "ImmediateOrCancel": "ioc",
    "FillOrKill": "fok"
  }
}
```

`day` expires at end of trading day; `gtc` stays active until filled/canceled (broker-specific limits apply).

## Trade unit

```json
{
  "TradeUnit": {
    "Dollars": "dollars",
    "Shares": "shares"
  }
}
```

`dollars` targets a notional amount; `shares` targets an explicit quantity.

## Trade status

```json
{
  "TradeStatus": {
    "Draft": "draft",
    "Placed": "placed",
    "PartiallyFilled": "partially_filled",
    "Complete": "complete",
    "Canceled": "canceled",
    "Failed": "failed",
    "Disconnected": "disconnected"
  }
}
```

`draft` usually means confirmation is still needed, while `placed` means it has already been submitted to the brokerage.

## Guidance

When the user names a brokerage in natural language, map it to the correct numeric `brokerageId` from this file instead of guessing.

When building orders, prefer enum values from this file over prose labels.