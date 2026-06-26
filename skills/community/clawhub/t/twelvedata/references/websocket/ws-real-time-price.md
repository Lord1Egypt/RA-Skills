# Twelve Data LLM Reference
> Last synced: 2026-03-29 20:21:15 UTC

# Real-time price (Useful)

**WebSocket URL:** `wss://ws.twelvedata.com/v1/quotes/price?apikey=your_api_key`

This method allows you to get real-time price streaming from the exchange. Equities also have day volume information.

**WebSocket credits cost:** `1` per symbol, API credits are not used

## Response

There are two general return event types: `status` and `price`.

Status events return the information about the events itself, which symbols were successfully subscribed/unsubscribed, etc.

Price events return the real-time tick prices for particular instruments. The body will include the meta information, UNIX timestamp, and the price itself. Price events return the real-time tick prices, with the following structure:

| Field*      | Description |
|-------------|-------------|
| event       | type of event |
| symbol      | symbol ticker of instrument |
| type        | general instrument type |
| timestamp   | timestamp in UNIX format |
| price       | real-time price for the underlying instrument |
| day_volume  | volume of the instrument for the current trading day |

*Some additional meta response field will be received, depending on the class of the instrument.

## Further steps

At this stage you might decide that you no longer want to be subscribed for particular symbols, therefore you have two options:
  1. Manually unsubscribe from symbols. This is done with the same format as the subscription, but with action set to `"action": "unsubscribe"`.
  2. Reset subscription. This will reset your current connection from all subscriptions. <br>Send the `{"action": "reset"}` event.

We also recommend sending `{"action": "heartbeat"}` events to the server every 10 seconds or so. This will make sure to keep your connection stable.

## Example requests

### Subscribe to multiple symbols

```
# You may subscribe to multiple symbols by
# calling subscribe action. Additionally,
# you can pass the exchange name after
# the colon(:).

{
  "action": "subscribe", 
  "params": {
    "symbols": "AAPL,RY,RY:TSX,EUR/USD,BTC/USD"
  }
}
```

### Subscribe using extended format

```
# Alternatively, if you need to get data from the 
# ambiguos symbol you may use the extended format

{ "action": "subscribe", 
  "params": {
    "symbols": [{
        "symbol": "AAPL",
        "exchange": "NASDAQ"
      }, {
        "symbol": "RY", 
        "mic_code": "XNYS"
      }, {
        "symbol": "EUR/USD",
        "type": "Forex"
      }
]}}
```




## Example responses

### Success subscription

```
{
  "event": "subscribe-status",
  "status": "ok",
  "success": [
    { 
      "symbol":"AAPL","exchange":"NASDAQ",
      "country":"United States",
      "type":"Common Stock"
    },
    { 
      "symbol":"RY","exchange":"NYSE",
      "country":"United States",
      "type":"Common Stock"
    },
    {
      "symbol":"RY","exchange":"TSX",
      "country":"Canada",
      "type":"Common Stock"
    },
    {
      "symbol":"EUR/USD","exchange":"FOREX",
      "country":"",
      "type":"Physical Currency"
    },
    {
      "symbol":"BTC/USD","exchange":"FOREX",
      "country":"",
      "type":"Physical Currency"
    }
  ],
  "fails": []
}
```

### Price event data response

```
{
  "event": "price",
  "symbol": "AAPL",
  "currency": "USD",
  "exchange": "NASDAQ",
  "type": "Common Stock",
  "timestamp": 1592249566,
  "price": 342.0157,
  "day_volume": 27631112
}
```

### Bid/Ask data response (where available)

```
{
  "event": "price",
  "symbol": "XAU/USD",
  "currency": "USD",
  "currency_base": "Gold Spot",
  "currency_quote": "US Dollar",
  "type": "Physical Currency",
  "timestamp": 1647950462,
  "price": 1925.18,
  "bid": 1925.05,
  "ask": 1925.32
}
```

