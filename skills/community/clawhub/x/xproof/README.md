# xProof — Prove Before Act for AI Agents

> **No API key needed.** Any agent can anchor a proof and pay per call via x402 — one HTTP request, no account, no setup.

The accountability layer for autonomous agents. Anchor reasoning (WHY) and action (WHAT) on-chain before execution. Immutable 4W audit trail on MultiversX.

## Install

```bash
# Via Hermes
hermes skills install clawhub/xproof

# Via OpenClaw
openclaw skills install xproof
```

## What is Prove Before Act?

1. Agent generates reasoning (WHY)
2. SHA-256 hash computed locally — raw content never leaves the machine
3. Hash + 4W metadata anchored on MultiversX before execution
4. Agent executes with `proof_id` attached
5. Public, immutable verification at `xproof.app/proof/{id}`

## Code Examples

### Python — x402 (no API key)

```python
import hashlib, json, base64, requests

def prove_before_act_x402(reasoning: dict, wallet_signer) -> dict:
    file_hash = hashlib.sha256(
        json.dumps(reasoning, sort_keys=True).encode()
    ).hexdigest()

    # POST without auth → HTTP 402 ($0.05 USDC on Base)
    r = requests.post("https://xproof.app/api/proof",
        json={"file_hash": file_hash, "filename": "reasoning.json"})
    assert r.status_code == 402

    signed = wallet_signer.sign_x402(r.json()["payment"])
    x_payment = base64.b64encode(json.dumps(signed).encode()).decode()

    # Resend with X-PAYMENT → proof_id returned immediately
    return requests.post("https://xproof.app/api/proof",
        headers={"X-PAYMENT": x_payment},
        json={"file_hash": file_hash, "filename": "reasoning.json"}).json()
```

### Python — API key (free trial)

```python
from xproof import xproof

# Get 10 free proofs: POST https://xproof.app/api/agent/register
# → { api_key: "pm_...", free_certifications: 10 }

proof = await xproof.anchor(
    content=reasoning,
    metadata={"who": "my-agent", "what": "execute_trade", "why": reasoning}
)
# → proceed with action only after proof confirmed
```

### MCP tool call

```json
{
  "name": "certify_file",
  "arguments": {
    "file_hash": "sha256_of_reasoning",
    "filename": "decision.json",
    "metadata": {
      "who": "my-agent-v2",
      "what": "BUY BTC 0.5",
      "why": "RSI=38, risk/reward 1:3"
    }
  }
}
```

### MCP server (full integration)

```python
from mcp import MCPServer, Tool
from xproof import xproof_x402

class xProofTool(Tool):
    name = "xproof_anchor"
    description = "Anchor reasoning (WHY) and planned action (WHAT) BEFORE execution. No API key — pays via x402."

    async def execute(self, reasoning: str, action: str, who: str):
        proof = await xproof_x402.anchor(
            content=f"Reasoning:\n{reasoning}\n\nAction:\n{action}",
            metadata={"who": who, "what": action, "why": reasoning},
            payment={"method": "x402", "network": "base", "max_amount_usd": 0.05}
        )
        return {"proof_id": proof.id, "verify_url": proof.verify_url}
```

## Pricing

| Volume | Price |
|--------|-------|
| 0 – 100k | $0.05 / proof |
| 100k – 1M | $0.025 / proof |
| 1M+ | $0.01 / proof |

**Free trial**: 10 proofs via `register_trial` MCP tool — no wallet, no card.

## Proven in Production

**xproof_agent_verify** (Moltbook) — 4,418 on-chain proofs, 100% confirmation rate, 16-week streak, trust score 43,326 Verified.

[View live agent profile →](https://xproof.app/agent/erd1hlx4xanncp2wm9aly2q6ywuthl2q9jwe9sxvxpx4gg62zcrvd0uqr8gyu9)

## Links

- [xProof Platform](https://xproof.app)
- [Agent Context Doc](https://xproof.app/agent-context) — 12 questions answered, x402 guide, honest assessment
- [MCP Endpoint](https://xproof.app/mcp)
- [API Docs](https://xproof.app/docs)
