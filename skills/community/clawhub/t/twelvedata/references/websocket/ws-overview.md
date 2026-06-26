# Twelve Data LLM Reference
> Last synced: 2026-03-29 20:21:15 UTC

# Overview

You may use the API key to connect to the Twelve Data Distributed WebSocket System (TDDWS). This system will manage all your requests to all available instruments across different exchanges. You can establish up to **3** connections (typically used in `production`, `stage`, and `local` environments) across the whole lifespan of the application; if you open more, the previous connections will be closed.

You may subscribe to all symbols available at Twelve Data; meanwhile, the format remains the same as the API unless there are constraints in the endpoint. Moreover, you may combine symbols across different types, and TDDWS will manage the routing. There are some limitations, though:
  - Server limits to receive up to `100` events from the client-side. This constraint does not affect the number of messages sent from the server to the client.
  - There is no limit on the number of input symbols; however, the size of the input message can not exceed `1 MB`.

Full WebSocket access is available on the **Pro** plan (individual) and **Venture** plan (business), and above. On Basic and Grow individual plans, testing is limited to one connection and up to 8 simultaneous symbol subscriptions from the permitted symbol list.

## Resources

You can try streaming via the [WebSocket Playground](https://twelvedata.com/account/websocket) in your dashboard. On Basic and Grow plans, only trial symbols are available. On the Pro plan (individual) and Venture plan (business) and above, any instrument can be streamed.

[Trial symbols](https://support.twelvedata.com/en/articles/5335783-trial)

[WebSocket FAQ](https://support.twelvedata.com/en/articles/5194610-websocket-faq)

[How to stream data tutorial](https://support.twelvedata.com/en/articles/5620516-how-to-stream-the-data)

## Example requests

### Connect & Authorize

```
# Pass API key as connection parameter
wss://ws.twelvedata.com/v1/{$route}?apikey=your_api_key

# Or pass API key separately in header
wss://ws.twelvedata.com/v1/{$route}
X-TD-APIKEY: your_api_key
```




