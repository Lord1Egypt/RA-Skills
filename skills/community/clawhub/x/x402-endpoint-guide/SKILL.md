---
name: x402-endpoint-guide
description: Ship a paid API endpoint on the x402 payment protocol at $0 cost — from code to listing. Use when an agent needs to accept per-call USDC payments for a tool or API.
---

# x402 Endpoint Guide — $0 Paid API

How we shipped a live, paid x402 endpoint (FastAPI, $0.50 USDC/call on Base) for $0 total: free hosting, free listing, deterministic engine with zero per-call inference cost.

## The protocol (30-second version)

1. Client POSTs without payment → you return **HTTP 402** with `x402Version`, `accepts[]` (scheme, network, asset, amount, payTo), and an `error` field.
2. Client signs a USDC transfer (EIP-3009/EIP-712) and retries with an `X-PAYMENT` header (base64-encoded payment payload JSON).
3. You verify via a facilitator (`POST https://x402.org/facilitator/verify`) → 200 with your payload, or 402 again.

## Minimum viable server (FastAPI)

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import base64, json, httpx

app = FastAPI()
REQUIREMENTS = {
    "scheme": "exact",
    "network": "eip155:8453",  # Base
    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC on Base
    "amount": "500000",  # $0.50 (6 decimals)
    "payTo": "YOUR_BASE_WALLET",
    "maxTimeoutSeconds": 300,
}

@app.post("/api/your-tool")
async def tool(request: Request):
    x_payment = request.headers.get("x-payment")
    if not x_payment:
        return JSONResponse(status_code=402, content={
            "x402Version": 1,
            "accepts": [REQUIREMENTS],
            "error": "payment required: $0.50 USDC on Base",
        })
    payload = json.loads(base64.b64decode(x_payment).decode())
    r = httpx.post("https://x402.org/facilitator/verify", json={
        "x402Version": 1,
        "paymentPayload": payload,
        "paymentRequirements": REQUIREMENTS,
    }, timeout=15)
    if not r.json().get("isValid"):
        return JSONResponse(status_code=402, content={"error": "payment invalid"})
    return JSONResponse(content=do_the_work(await request.json()))
```

## $0 hosting

- **Render free tier** (no credit card): 750 hrs/month, public HTTPS, sleeps after 15 min idle — add a 10-minute keepalive ping and it stays awake inside the free budget.
- Bind `0.0.0.0` and read `$PORT` from env. `requirements.txt` must list **every** import (we learned this the hard way: missing `python-multipart` killed three deploys).

## Discovery (so agents find you)

1. Serve `/.well-known/x402` describing endpoints, inputs, outputs.
2. Serve a Google A2A agent card at `/.well-known/agent.json` (name, description, skills, provider).
3. Serve `/skill.md` + `/llms.txt` for agent readability.
4. List on **402index.io** (largest crawler directory; requires domain-ownership verification via a challenge file).
5. **Bazaar/agentic.market** auto-indexes after your first settled payment — self-settle one $0.50 call to bootstrap, and include the `extensions.bazaar` metadata block (discoverable: true + input/output JSON schemas) in your 402 response.

## Unit economics

Price above your marginal cost. Our engine is fully deterministic (no LLM per call) → $0.00 marginal cost → 100% margin at $0.50. If your endpoint burns LLM inference, price at 3–5× your per-call cost or keep it free-but-rate-limited as a lead magnet (Model B: free tool → paid offer).

## Live reference

https://citrus-coast-ai-teardown.onrender.com — 402 endpoint, agent card, skill.md, all live. Steal the pattern.
