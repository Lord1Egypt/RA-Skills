--s--BCL25,BASE64
name: xproof
version: 4.0.0
description: "No API key needed. Any agent can anchor a proof and pay per call via x402 — one HTTP request, no account, no setup. Prove Before Act: anchor reasoning (WHY) on-chain before executing (WHAT). 4W immutable audit trail on MultiversX. MCP native."
homepage: https://xproof.app
metadata: {"xproof":{"category":"proof,security,compliance,accountability,x402,mcp","api_base":"https://xproof.app","x402":true,"mcp":true,"prove_before_act":true}}
---

# xProof — Prove Before Act for AI Agents

> **No API key needed.** Any agent can anchor a proof and pay per call via x402 — one HTTP request, no account, no setup.

The accountability layer for autonomous agents. Instead of being a black box, your agent becomes transparent, auditable, and verifiable.

**Prove Before Act**: anchor your agent's reasoning (WHY) and planned action (WHAT) on-chain *before* executing. Hash is computed locally — no raw content ever leaves the agent.

**Proven in production**: xproof_agent_verify (Moltbook) — 4,418 on-chain proofs, 100% confirmation rate, 16-week streak, trust score 43,326. $0.05/proof, ~$13.80/week for a continuously accountable agent.

---

## Why it matters in 2026

- **AI Act compliance** — traceable decision audit trail before every action
- **Legal & reputational accountability** — immutable evidence of what the agent decided and why
- **User & enterprise trust** — public verifiable proofs, not internal logs anyone can edit

---

## Key features

- **Privacy-first** — only SHA-256 hash anchored on-chain, raw content stays local
- **x402 native** — pay per call with USDC on Base, no API key, no account, no human
- **MCP compatible** — JSON-RPC 2.0 endpoint, tools: `certify_file`, `audit_agent_session`, `investigate_proof`, `register_trial`
- **4W audit trail** — Who, What, When, Why — publicly verifiable at `xproof.app/proof/{id}`
- **Free trial** — 10 free proofs via `register_trial` MCP tool or `POST /api/agent/register`, no wallet

---

## Install

```bash
# Via Hermes
hermes skills install clawhub/xproof

# Via OpenClaw
openclaw skills install xproof
```

---

## Code examples

### 1. Basic (Python + API key)

```python
from xproof import xproof

async def prove_before_act(task):
    reasoning = await agent.think(task)

    # Prove Before Act — anchor reasoning BEFORE execution
    proof = await xproof.anchor(
        content=reasoning,
        metadata={
            "who": "my-agent-v1",
            "what": f"execute task: {task}",
            "why": reasoning,
            "purpose": "decision_audit"
        }
    )

    # Only execute after proof is confirmed
    result = await agent.execute(task, proof_id=proof.id)
    print(f"Proof: https://xproof.app{proof.verify_url}")
    return result
```

### 2. Via x402 (no API key — fully autonomous)

```python
import hashlib, json, base64, requests

def prove_before_act_x402(reasoning: dict, wallet_signer) -> dict:
    """No API key, no account — pure machine-to-machine."""
    # 1. Hash locally
    file_hash = hashlib.sha256(
        json.dumps(reasoning, sort_keys=True).encode()
    ).hexdigest()

    # 2. POST without auth → HTTP 402 with price ($0.05 USDC on Base)
    r = requests.post("https://xproof.app/api/proof",
        json={"file_hash": file_hash, "filename": "reasoning.json"})
    assert r.status_code == 402  # ← x402 challenge

    # 3. Sign USDC on Base (eip155:8453)
    signed = wallet_signer.sign_x402(r.json()["payment"])
    x_payment = base64.b64encode(json.dumps(signed).encode()).decode()

    # 4. Resend with X-PAYMENT → proof_id returned immediately
    proof = requests.post("https://xproof.app/api/proof",
        headers={"X-PAYMENT": x_payment},
        json={"file_hash": file_hash, "filename": "reasoning.json"})

    return proof.json()  # { proof_id, verify_url }
```

### 3. Via MCP tool call

```json
// Call certify_file before any significant action
{
  "name": "certify_file",
  "arguments": {
    "file_hash": "sha256_of_reasoning",
    "filename": "decision_reasoning.json",
    "metadata": {
      "who": "my-agent-v2",
      "what": "execute trade BUY BTC 0.5",
      "why": "RSI=38, below oversold threshold, risk/reward 1:3",
      "purpose": "prove_before_act"
    }
  }
}
// Returns: { proof_id, verify_url, status: "anchored" }
// → Now execute the action with proof_id attached
```

### 4. Full MCP server integration

```python
from mcp import MCPServer, Tool
from xproof import xproof_x402

class xProofTool(Tool):
    name = "xproof_anchor"
    description = "Anchor agent reasoning (WHY) and planned action (WHAT) BEFORE execution. No API key — pays via x402."

    async def execute(self, reasoning: str, action: str, who: str):
        proof = await xproof_x402.anchor(
            content=f"Reasoning:\n{reasoning}\n\nAction:\n{action}",
            metadata={"who": who, "what": action, "why": reasoning},
            payment={"method": "x402", "network": "base", "max_amount_usd": 0.05}
        )
        return {
            "status": "anchored",
            "proof_id": proof.id,
            "verify_url": proof.verify_url,
            "message": "Reasoning anchored. Proceed with action."
        }

server = MCPServer("xproof-accountability")
server.register_tool(xProofTool())
```

---

## Use cases

- Trading & finance agents (prove risk assessment before execution)
- Research agents (certify findings before publishing)
- Content agents (prove AI-generation metadata before publication — see Moltbook)
- Enterprise agents (compliance gate before any high-stakes action)
- Any agent that takes decisions with legal, financial, or reputational impact

---

## Pricing

| Volume | Price per proof |
|--------|----------------|
| 0 – 100k | $0.05 |
| 100k – 1M | $0.025 |
| 1M+ | $0.01 |

Free trial: 10 proofs via `register_trial` MCP tool — no wallet, no credit card.

---

## Links

- Platform: https://xproof.app
- Agent context doc: https://xproof.app/agent-context
- MCP endpoint: https://xproof.app/mcp
- Live agent profile (Moltbook): https://xproof.app/agent/erd1hlx4xanncp2wm9aly2q6ywuthl2q9jwe9sxvxpx4gg62zcrvd0uqr8gyu9
- x402 guide: https://xproof.app/agent-context#x402
