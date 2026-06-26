---
name: quantum-bridge
description: Transpile quantum circuits between Qiskit (OpenQASM) and OriginIR, run IBC multi-agent consensus, validate OriginIR, and submit circuits to real quantum hardware (Wukong 72Q chip) via the Quantum Bridge API. Use when a user asks to convert quantum circuits, run quantum consensus, submit to quantum hardware, check quantum backends, or work with OriginIR/OpenQASM formats.
---

# Quantum Bridge

Translates quantum circuits between frameworks and runs them on real hardware via the Quantum Bridge API at `quantum-api.gpupulse.dev`.

## Setup

Requires an API key. Get one free (50 credits) at https://quantum-api.gpupulse.dev

Store the key:
```bash
# In your TOOLS.md or env
QUANTUM_BRIDGE_KEY=qb_...
```

## API Reference

Base URL: `https://quantum-api.gpupulse.dev/api/v1`
Auth: `Authorization: Bearer qb_...` or `X-API-Key: qb_...`

### Transpile QASM → OriginIR (1 credit)

```bash
curl -X POST "$BASE/transpile" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"qasm": "OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q[0] -> c[0];\nmeasure q[1] -> c[1];"}'
```

Response: `{"originir": "QINIT 2\nCREG 2\nH q[0]\nCNOT q[0], q[1]\n...", "stats": {...}, "credits_charged": 1}`

### Reverse: OriginIR → QASM (1 credit)

```bash
curl -X POST "$BASE/reverse" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"originir": "QINIT 2\nCREG 2\nH q[0]\nCNOT q[0], q[1]"}'
```

### Validate OriginIR (free)

```bash
curl -X POST "$BASE/validate" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"originir": "QINIT 2\nH q[0]\nCNOT q[0], q[1]"}'
```

### IBC Consensus (2 credits)

Multi-agent quantum consensus. Each agent has a name and feature vector.

```bash
curl -X POST "$BASE/consensus" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"agents": [
    {"name": "Scheduler", "features": [0.9, 0.1, 0.3]},
    {"name": "Optimizer", "features": [0.1, 0.9, 0.2]},
    {"name": "Monitor",   "features": [0.7, 0.3, 0.5]}
  ], "threshold": 0.3}'
```

Response includes consensus groups, conflicts, similarity matrix, and quantum timing.

### Submit Circuit to Hardware (5-10 credits)

Submit to cloud simulator (5 credits) or real Wukong 72-qubit chip (10 credits).

```bash
curl -X POST "$BASE/submit" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"qasm": "OPENQASM 2.0;...", "backend": "wukong", "shots": 1000}'
```

Response: `{"task_id": "task_...", "status": "queued", "poll_url": "/api/v1/submit/task_..."}`

Poll for results:
```bash
curl "$BASE/submit/task_..." -H "Authorization: Bearer $KEY"
```

### Check Balance (free)

```bash
curl "$BASE/balance" -H "Authorization: Bearer $KEY"
```

### List Backends (free with auth)

```bash
curl "$BASE/backends" -H "Authorization: Bearer $KEY"
```

### Supported Gates (no auth)

```bash
curl "$BASE/gates"
```

## Supported Gates

20+ mappings: H, X, Y, Z, S, T, I, RX, RY, RZ, U2, U3, CNOT, CZ, SWAP, CR, Toffoli, CSWAP, DAGGER blocks, BARRIER, MEASURE.

## Usage Patterns

**Transpile for a user:**
1. Take their QASM input
2. POST to `/transpile`
3. Return the OriginIR and stats

**Run on real quantum hardware:**
1. POST to `/submit` with `"backend": "wukong"`
2. Get `task_id`
3. Poll `/submit/<task_id>` until `status` is `completed`
4. Return the measurement counts

**Multi-agent consensus:**
1. Collect agent names + feature vectors
2. POST to `/consensus`
3. Report groups, conflicts, and overlap scores

## Credit Costs

| Endpoint | Credits |
|----------|---------|
| transpile | 1 |
| reverse | 1 |
| validate | 0 |
| consensus | 2 |
| submit (simulator) | 5 |
| submit (wukong) | 10 |

## Pricing

- Free: 50 credits
- Starter: 500 credits — $5 USDC
- Pro: 5,000 credits — $25 USDC
- Enterprise: 50,000 credits — $100 USDC

Payment: USDC on Solana (contact for details)
