---
name: sigui-security
version: "2.0.1"
description: >
  AI security oracle for blockchain transactions. Evaluates EVM, Starknet, and Aptos
  transactions in real time using the Sigui Protocol — detecting drain stars, mixer chains,
  Sybil swarms, and flash-loan exploits before execution. Returns ALLOW / BLOCK / ESCALATE
  with an on-chain proof. Requires a real Sigui API endpoint; demo mode available for testing.
author: "Warma Abdoul Ibonon Eric <ericwarma2006@gmail.com>"
homepage: "https://github.com/ibonon/Sigui"
license: MIT
tags:
  - blockchain
  - security
  - web3
  - defi
  - ai-agent
  - ethereum
  - starknet
  - aptos
read_when:
  - The user explicitly asks to evaluate, audit, or check the safety of a specific blockchain transaction before sending it
  - The user says "check this address", "is this contract safe", or "evaluate this transaction" and provides concrete parameters (address, amount, chain)
  - The user reports a suspected rug pull, drain attack, phishing approval, or flash-loan exploit they want analyzed
  - An autonomous agent is about to submit an on-chain transaction and needs security clearance
install:
  run: bash install.sh
requires:
  python: ">=3.10"
  packages:
    - "sigui-sdk>=0.3.1"
    - "rich>=13.0.0"
---

# Sigui Protocol Security Skill 🛡️

**Sigui** is a multi-chain AI security oracle that evaluates blockchain transactions before
they execute, using a native Spatio-Temporal Transformer (Trustformer/T-GAT) to detect
coordinated attacks in real time.

> [!IMPORTANT]
> **This skill requires a real Sigui API endpoint for production use.**
> Set `SIGUI_API_URL` to your node URL. Without it, the script exits safely (fail-closed).
> A `--demo` flag is available for testing, but MUST NOT be used to authorize real funds.

---

## 🔐 Security Model

This skill is designed with a **fail-closed** security policy:

| Situation | Behavior |
|-----------|----------|
| No API URL configured | ❌ Exits with error — does NOT simulate |
| API unreachable | ❌ Exits with error — does NOT simulate |
| ALLOW verdict | ⏸️ Pauses and asks for **explicit user confirmation** |
| BLOCK verdict | 🚫 Immediately returns exit code 1 |
| ESCALATE verdict | 🔍 Requests deep analysis with `--escalate` |
| `--demo` flag set | ⚠️ Shows prominent warning — heuristic only |

---

## 🧠 Agent Instructions (Chain of Thought)

When a user explicitly asks to evaluate a specific transaction, follow these steps:

### Step 1 — Extract Parameters
Identify from the user's message:
- `amount`: transaction value (convert to USDC equivalent if needed)
- `destination`: the target wallet or contract address
- `chain`: the blockchain (default `arc`)
- `action`: the action type (`transfer`, `approve`, `swap`, `bridge`, `mint`)

If any required parameter is missing, **ask the user** before running the evaluation.

### Step 2 — Ask for Explicit Confirmation Before Running
Before executing the script, show the user:
> "I'm about to evaluate this transaction with the Sigui security oracle:
> - Amount: {amount} USDC
> - Destination: {destination}
> - Chain: {chain}
> - Action: {action}
> Shall I proceed?"

### Step 3 — Run the Evaluation
```bash
python ~/.openclaw/workspace/skills/sigui-security/evaluate.py \
  --amount {amount} \
  --destination {destination} \
  --action {action} \
  --chain {chain}
```

### Step 4 — Interpret the Exit Code

| Exit Code | Verdict | Agent Action |
|-----------|---------|--------------|
| `0` | ALLOW | Ask user: *"Sigui approves. Do you confirm the transaction?"* Only proceed if user says yes. |
| `1` | BLOCK | 🚫 **ABORT.** Tell the user the threat detected. Do NOT proceed. |
| `2` | ESCALATE | Ask user if they want deep analysis, then re-run with `--escalate`. |
| `3` | Error | Report the error. Do NOT proceed with the transaction. |

### Step 5 — After ALLOW: Require User Confirmation
Re-run with `--confirmed` **only after the user explicitly says yes**:
```bash
python evaluate.py --amount {amount} --destination {destination} \
  --action {action} --chain {chain} --confirmed
```

---

## 🛠️ Setup

### 1. Install Dependencies (automatic)
The skill auto-installs `sigui-sdk` when first run. Or run manually:
```bash
bash ~/.openclaw/workspace/skills/sigui-security/install.sh
```

### 2. Configure Your Sigui Endpoint (required for production)
```bash
export SIGUI_API_URL="https://your-sigui-node.com"
export SIGUI_CHAIN="arc"           # Optional, default: arc
export OPENCLAW_AGENT_ID="my_agent"  # Optional
```

### 3. Test in Demo Mode (non-authoritative)
```bash
python evaluate.py --amount 50 --destination 0xYourAddress --demo
```
> ⚠️ Demo mode output is a local heuristic simulation, NOT an oracle evaluation.
> Never use demo results to authorize transactions.

---

## 📊 Verdict Table

| Verdict | Risk Score | Meaning |
|---------|-----------|---------|
| `ALLOW` | 0.0–0.35 | Transaction appears safe — **await user confirmation** |
| `ALLOW_WITH_CAP` | 0.35–0.55 | Safe up to spending cap — **await user confirmation** |
| `ESCALATE` | 0.55–0.80 | Ambiguous — request deep analysis before deciding |
| `BLOCK` | 0.80–1.0 | Threat detected — do NOT proceed |

**Safety Score** = `(1 - risk_score) × 1000`. Higher = safer.

---

## 🛡️ Threats Detected

| Attack | Description |
|--------|-------------|
| Drain Star | Orchestrator draining multiple wallets simultaneously |
| Mixing Chain | Layered hops through mixers to obscure fund origin |
| Sybil Swarm | Fake-identity cluster attacking governance or airdrops |
| Flash Loan Exploit | Oracle price manipulation within one atomic block |
| Honeypot Contract | Buy-enabled, sell-disabled token trap |
| Rug Pull | Liquidity removal by deployer |
| Phishing Signature | Malicious `eth_sign` / `permit` approval |

---

## 🔗 Links

- 📄 **GitHub**: https://github.com/ibonon/Sigui
- 📦 **PyPI**: https://pypi.org/project/sigui-sdk/
- 🌐 **ClawHub**: https://clawhub.ai/ibonon/sigui-security
- 📖 **Whitepaper**: *Sigui Protocol: A Real-Time Security Oracle for Autonomous AI Agents*
