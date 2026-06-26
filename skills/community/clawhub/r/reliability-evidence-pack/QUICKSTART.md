# REP Quickstart Guide

## What is REP?

REP (Reliability Evidence Pack) is a structured framework for capturing, validating, and reporting agent reliability artifacts. It provides tamper-evident logging for critical agent decisions, heartbeats, handoffs, and capability degradation tracking—essential for debugging, auditing, and proving system reliability.

## Quick Start Commands

```bash
# Navigate to your workspace
cd /home/qq1028280994/.openclaw/workspace

# Initialize a new REP bundle
node scripts/rep.mjs init my-incident --strict --description "Database migration incident"

# Emit an artifact (heartbeat, decision, handoff, etc.)
node scripts/rep.mjs emit --type heartbeat --session sess-123 --actor agent:christine --output artifacts/heartbeat.jsonl

# Validate the bundle
node scripts/rep.mjs validate rep-bundle/artifacts/heartbeat.jsonl

# View bundle statistics
node scripts/rep.mjs stats rep-bundle/
```

## Example Workflow

### Step 1: Initialize a Bundle

```bash
node scripts/rep.mjs init incident-2026-03-02 --strict --description "Post-deployment reliability check"
```

This creates a new bundle with a manifest and artifacts directory.

### Step 2: Emit Artifacts

Emit a heartbeat to prove the agent was operational:

```bash
node scripts/rep.mjs emit --type heartbeat --session sess-001 --actor agent:christine --output artifacts/agent_heartbeat_record.jsonl
```

Emit a decision log for a significant choice:

```bash
node scripts/rep.mjs emit --type decision --session sess-001 --actor agent:christine --output artifacts/decision_rejection_log.jsonl --summary "Rejected unsafe command injection"
```

### Step 3: Validate

Validate a single artifact:

```bash
node scripts/rep.mjs validate artifacts/agent_heartbeat_record.jsonl
```

Validate the entire bundle with chain and cross-reference checks:

```bash
node scripts/rep.mjs validate . --require-pack --check-chain --xref
```

### Step 4: View Stats

```bash
node scripts/rep.mjs stats .
```

## Available Artifact Types

- `heartbeat` — Agent operational proof
- `decision` — Significant agent decisions
- `handoff` — Task transfer records
- `degradation` — Capability degradation tracking
- `context_snapshot` — Runtime context captures

## More Documentation

- [SPEC.md](./SPEC.md) — Full specification
- [INTEGRATION.md](./INTEGRATION.md) — Workflow integration guide
- [Examples](./examples/) — Sample artifacts and use cases

---

*REP v1.0 — Built for agent reliability evidence*
