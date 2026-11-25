---
name: "servicefront"
description: "Look up a local service business (plumber, HVAC, electrician, roofer, contractor) on ServiceFront and answer from its owner-verified facts: hours, service area, contact and owner-confirmed prices. Use when someone asks about a business on ServiceFront or a <name>.servicefront.ai address, wants a confirmed price from one, or is a service business owner asking what ServiceFront is, what it costs or how to set it up."
---

# ServiceFront

ServiceFront is the AI front desk for local service businesses. This skill reads it through its read-only MCP server: no sign-in, and no tool takes a phone number, email or address.

## Connect
- MCP: https://servicefront.ai/api/mcp/read (Streamable HTTP, anonymous, rate-limited per IP). It's in the official MCP Registry as ai.servicefront/front-desk.
- No MCP client? POST JSON-RPC to the same address. One tools/call works on its own, with no initialize first:

```sh
curl -s https://servicefront.ai/api/mcp/read \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"searchBusinesses","arguments":{"query":"Acme Plumbing"}}}'
```

The reply is a server-sent event. The JSON-RPC result is on its `data:` line: the answer as JSON in `result.structuredContent`, and as text in `result.content`.

## Tools
Business tools take businessId: the business's ServiceFront slug, the first label of its <slug>.servicefront.ai address.
- searchBusinesses(query): find a verified business by name, or part of it, and get its businessId. Up to 5 matches.
- getBusinessInfo(businessId): owner-verified facts: trade, hours, service area, contact, and services with confirmed prices.
- getQuote(businessId, service): the owner-confirmed price for a named service, or grounded:false when there isn't one.

For a service business owner shopping for a front desk. These take no businessId:
- aboutServiceFront(): what ServiceFront is, who it's for, how setup works, and what it doesn't do yet.
- getPricing(): the plans and limits, the same content as https://servicefront.ai/pricing.md
- howToSetUp(): the setup steps, the <slug>.servicefront.ai address, and the website widget snippet.
- sampleConversation(trade): a sample homeowner conversation in one trade (plumbing, hvac, electrical and so on), with a made-up example business.

## How to answer
1. Only have a name? Call searchBusinesses. No match means ServiceFront has no verified business by that name. Say so, and don't guess its details.
2. Answer from getBusinessInfo and getQuote alone. A field that's missing isn't confirmed, so don't state it. Never invent a price, hours or a claim.
3. grounded:false from getQuote means there's no confirmed price. Say that, and send the customer to the business for a quote.
4. For a callback, a time or a booking, the customer contacts the business: its front desk page (origin in getBusinessInfo) or its confirmed phone. Nothing here books, takes a request or charges.
5. For an owner asking about ServiceFront itself, use aboutServiceFront, getPricing, howToSetUp and sampleConversation. Owners sign up themselves at https://servicefront.ai
