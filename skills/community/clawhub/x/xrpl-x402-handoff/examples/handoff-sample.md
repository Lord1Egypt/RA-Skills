# Usage example (blind)

**Trigger:** “We got 402 on mainnet, paid once, verify says tx not found — what now?”

**Expected shape:**

```
Network: xrpl
Facilitator: https://api.xrplfi.com
SellerId / OriginUrl: (from catalog)
Scheme chosen: exact
Action: retry-same-header
TxHash or ChannelId: <existing hash only>
Spend this call / session: unchanged — do not pay again
Handoff owner: —
Do-not-do: do not submit a second Payment for the same nonce
Next human step: wait 2–3s; retry identical X-PAYMENT; if still failing after backoff, escalate to ops with hash + nonce expiry
```
