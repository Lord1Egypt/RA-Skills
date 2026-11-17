---
name: twzrd-preflight
description: Use when configuring OpenClaw to run TWZRD preflight checks before payment-shaped x402 tool calls.
---

# TWZRD Preflight

Use `twzrd-preflight` when an OpenClaw operator wants a native `before_tool_call`
gate for payment-shaped x402 or AgentCash-style tool calls.

The runtime plugin is installed from npm:

```bash
npm install twzrd-preflight
```

OpenClaw config example:

```json
{
  "plugins": [
    {
      "name": "twzrd-preflight",
      "config": {
        "mode": "enforce",
        "failMode": "closed",
        "refuseWashFlagged": true,
        "endpoint": "https://intel.twzrd.xyz"
      }
    }
  ]
}
```

Factory defaults are enforce + fail-closed + wash refuse. Assign
`wrapFetchWithTwzrdPreflight(fetch)` on the HTTP client so a 402 wash payTo
cannot reach a signer. `mode: "shadow"` is opt-in (log only).

The remote preflight endpoint is free. Paid trust receipts remain available from
`https://intel.twzrd.xyz` for agents that need portable proof.
