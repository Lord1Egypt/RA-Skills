---
name: tidb-x
description: TiDB X — object-storage-native distributed SQL for AI agent workloads. Use when building agent memory, context storage, multi-agent coordination, Web3 indexing, or any durable queryable state for AI systems.
---

# TiDB X

**Object-storage-native, elastic, multi-tenant SQL engine for AI agents. Charged-by-query (RU).**

## Quick Start (TiDB Cloud Zero)

Get a free MySQL-compatible database instantly. No sign-up, no billing.

```bash
# Provision (single API call, no auth required)
curl -s -X POST "https://zero.tidbapi.com/v1alpha1/instances" \
  -H "Content-Type: application/json" \
  -d '{"tag":"my-agent"}' | tee tidb-zero.json

# Response includes: host, port, username, password, expiresAt, claimUrl
# Extract connection info
jq -r '.instance.connectionString' tidb-zero.json

# Connect (always use TLS)
export MYSQL_PWD=$(jq -r '.instance.connection.password' tidb-zero.json)
mysql -u $(jq -r '.instance.connection.username' tidb-zero.json) \
  -h $(jq -r '.instance.connection.host' tidb-zero.json) \
  -P 4000 --ssl-mode=REQUIRED
```

**Claim your instance:** The response includes `claimInfo.claimUrl` — open it to convert the ephemeral instance into a permanent **TiDB Cloud Starter** (free). Without claiming, it auto-expires in 30 days.

```bash
# Get claim URL
jq -r '.instance.claimInfo.claimUrl' tidb-zero.json
```

Or sign up directly at https://tidbcloud.com/free-trial/

---

## When To Use TiDB X

Use it when your agent needs state that is:
- **Durable** — survives crashes, restarts, device failure
- **Shared** — multiple agents read/write the same data
- **Isolated** — per-user or per-agent data separation
- **Queryable** — SQL queries, not just key-value lookup
- **Auditable** — who did what, when, and why
- **Elastic** — scales with bursty, unpredictable agent traffic
- **Cost-efficient** — pay per query, not per idle instance

**Don't use it for:** ephemeral scratchpads, pure in-memory cache, fully offline single-device apps.

---

## Mental Model

```
Agent writes SQL
      │
      ▼
TiDB Server (stateless, parses + optimizes SQL)
      │
      ▼
TiKV (hot cache, ack to agent fast)
      │
      ▼
S3 Object Storage (source of truth, durable, cheap, infinite)
      │
      ▼
Background Pool (compaction, DDL — isolated, never blocks your queries)
```

Key ideas:
- **S3 is the source of truth** — not local disks
- **Compute is stateless** — scale up/down without data migration
- **Background work is isolated** — compaction never spikes your latency
- **RU billing** — every query has a cost in Request Units; idle = free

---

## Patterns (Copy-Paste Ready)

### Pattern 1: Agent Memory

Store and query agent memories. Works for support bots, coding agents, personal assistants.

```sql
CREATE TABLE agent_memory (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  tenant_id VARCHAR(64),
  agent_id VARCHAR(64),
  type VARCHAR(32),
  content TEXT,
  tags JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_tenant (tenant_id)
);

-- Store a memory
INSERT INTO agent_memory (tenant_id, agent_id, type, content, tags)
VALUES ('user_123', 'support_bot', 'resolution',
  'Customer frustrated about billing. Offered 20% discount.',
  '["billing", "discount", "escalation"]');

-- Query memories
SELECT content, created_at FROM agent_memory
WHERE tenant_id = 'user_123' ORDER BY created_at DESC LIMIT 10;

-- Search by tag
SELECT * FROM agent_memory
WHERE tenant_id = 'user_123' AND JSON_CONTAINS(tags, '"billing"');
```

---

### Pattern 2: Session Context (Append-Only)

For coding agents, research agents, or any long-running task. Append-only, never update.

```sql
CREATE TABLE agent_context (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  session_id VARCHAR(128),
  step INT,
  type VARCHAR(32),       -- 'observation', 'tool_call', 'tool_output', 'decision'
  content TEXT,
  tokens INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_session (session_id, step)
);

-- Append a step
INSERT INTO agent_context (session_id, step, type, content, tokens)
VALUES ('task_abc', 42, 'tool_output', '{"file": "auth.ts", "result": "ok"}', 800);

-- Resume after crash: reload recent steps + all decisions
SELECT * FROM agent_context
WHERE session_id = 'task_abc'
AND (step > 30 OR type = 'decision')
ORDER BY step ASC;
```

---

### Pattern 3: Multi-Agent Task Queue

Prevent duplicate work when multiple agents run in parallel.

```sql
CREATE TABLE tasks (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  task_key VARCHAR(255) UNIQUE,
  status VARCHAR(32) DEFAULT 'pending',
  agent_id VARCHAR(64),
  input JSON,
  output JSON,
  claimed_at TIMESTAMP NULL,
  completed_at TIMESTAMP NULL,
  INDEX idx_status (status)
);

-- Claim a task (atomic — only one agent wins)
UPDATE tasks SET status = 'claimed', agent_id = 'worker_3', claimed_at = NOW()
WHERE task_key = 'enrich:Union.ai' AND status = 'pending';

-- Complete
UPDATE tasks SET status = 'done',
  output = '{"investors": "NEA, Insight Partners"}',
  completed_at = NOW()
WHERE task_key = 'enrich:Union.ai' AND agent_id = 'worker_3';
```

---

### Pattern 4: Auditable Decisions (Provenance)

When you need to explain why an agent did something.

```sql
CREATE TABLE agent_decisions (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  tenant_id VARCHAR(64),
  agent_id VARCHAR(64),
  action VARCHAR(32),
  reasoning TEXT,
  source JSON,            -- {"guideline": "WHO-2026", "confidence": 0.92}
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_tenant (tenant_id)
);

-- Record a decision with reasoning
INSERT INTO agent_decisions (tenant_id, agent_id, action, reasoning, source)
VALUES ('patient_456', 'med_bot', 'recommend',
  'HbA1c = 7.8%, above 7% threshold. Recommending metformin per WHO guideline.',
  '{"guideline": "WHO-2026-diabetes", "confidence": 0.92}');

-- Audit trail
SELECT action, reasoning, source, created_at FROM agent_decisions
WHERE tenant_id = 'patient_456' ORDER BY created_at DESC;
```

---

### Pattern 5: Blockchain Event Indexing (Web3)

Monitor and correlate on-chain activity across multiple chains.

```sql
CREATE TABLE chain_events (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  chain VARCHAR(16),
  tx_hash VARCHAR(128),
  block_number BIGINT,
  from_addr VARCHAR(64),
  to_addr VARCHAR(64),
  value_wei VARCHAR(78),
  method VARCHAR(64),
  agent_id VARCHAR(64),
  tags JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_chain_block (chain, block_number),
  INDEX idx_addr (from_addr)
);

-- Index a whale swap
INSERT INTO chain_events (chain, tx_hash, block_number, from_addr, to_addr,
  value_wei, method, agent_id, tags)
VALUES ('ethereum', '0xabc...', 19500000, '0xwhale...', '0xuniswap...',
  '50000000000000000000', 'swap', 'whale_watcher', '["whale", "defi"]');

-- Find whale activity
SELECT chain, method, value_wei FROM chain_events
WHERE JSON_CONTAINS(tags, '"whale"') ORDER BY created_at DESC;

-- Cross-chain: same wallet on multiple chains
SELECT chain, COUNT(*) as txns FROM chain_events
WHERE from_addr = '0xwhale...' GROUP BY chain;
```

---

### Pattern 6: DeFi Portfolio Agent (Web3)

Track positions, strategies, and exit decisions with full reasoning.

```sql
CREATE TABLE defi_positions (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  tenant_id VARCHAR(64),
  protocol VARCHAR(64),
  chain VARCHAR(16),
  position_type VARCHAR(32),
  token_pair VARCHAR(64),
  amount DECIMAL(36,18),
  entry_price DECIMAL(36,18),
  current_value DECIMAL(36,18),
  strategy JSON,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_tenant (tenant_id)
);

-- Agent exits a position and explains why
INSERT INTO agent_decisions (tenant_id, action, reasoning, source)
VALUES ('wallet_0x123', 'exit_lp',
  'Impermanent loss hit 5.2% on ETH/USDC. Threshold is 5%. Exiting.',
  '{"tx_hash": "0xdef...", "profit_loss": -234.56}');

-- User asks: "Why did you sell?"
SELECT action, reasoning, created_at FROM agent_decisions
WHERE tenant_id = 'wallet_0x123' ORDER BY created_at DESC LIMIT 1;
```

---

### Pattern 7: Smart Contract Event Decoder (Web3)

Index contract events with AI-generated interpretations.

```sql
CREATE TABLE contract_events (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  chain VARCHAR(16),
  contract_addr VARCHAR(64),
  event_name VARCHAR(128),
  decoded_args JSON,
  block_number BIGINT,
  block_timestamp TIMESTAMP,
  agent_interpretation TEXT,
  INDEX idx_contract (contract_addr, event_name)
);

-- Index with interpretation
INSERT INTO contract_events (chain, contract_addr, event_name,
  decoded_args, block_number, block_timestamp, agent_interpretation)
VALUES ('ethereum', '0xUniV3...', 'Swap',
  '{"tokenIn": "USDC", "amountIn": 5000000, "tokenOut": "ETH", "amountOut": 2.45}',
  19500000, NOW(),
  'Large USDC→ETH swap ($5M). Possible institutional accumulation.');

-- Aggregate swaps
SELECT SUM(CAST(JSON_EXTRACT(decoded_args, '$.amountOut') AS DECIMAL(36,18))) as total_eth
FROM contract_events
WHERE contract_addr = '0xUniV3...' AND event_name = 'Swap'
AND JSON_EXTRACT(decoded_args, '$.tokenOut') = 'ETH';
```

---

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │          AI Agent Layer              │
                    │  Agent A   Agent B   Agent C  ...   │
                    └───────┬───────┬───────┬─────────────┘
                            │       │       │
                            ▼       ▼       ▼
                    ┌─────────────────────────────────────┐
                    │        TiProxy / Gateway            │
                    │   Connection routing, balancing     │
                    └───────────────┬─────────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           ▼                        ▼                        ▼
  ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
  │  TiDB Server   │      │  TiDB Server   │      │  TiDB Server   │
  │  (Stateless)   │      │  (Stateless)   │      │  (Stateless)   │
  └───────┬────────┘      └───────┬────────┘      └───────┬────────┘
          └───────────────────────┼───────────────────────┘
                                  │
           ┌──────────────────────┼──────────────────────┐
           ▼                      ▼                      ▼
  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
  │  TiKV (Cache)  │    │  TiKV (Cache)  │    │  TiKV (Cache)  │
  └───────┬────────┘    └───────┬────────┘    └───────┬────────┘
          └───────────────────────┼──────────────────────┘
                                  ▼
  ┌──────────────────────────────────────────────────────────┐
  │              Object Storage (S3)                          │
  │              Source of truth • Durable • Infinite          │
  └──────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────┐
  │         Background Compute (Isolated from OLTP)           │
  │   Compaction │ Import │ DDL │ Stats — never blocks you    │
  └──────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────┐
  │         TiCI — Pluggable Index Engines                    │
  │   Columnar (analytics) │ Inverted (search) │ Vector (AI)  │
  └──────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────┐
  │         RU Metering — Per-query cost attribution          │
  │   Query → 12 RU │ Query → 340 RU │ Idle → 0 RU           │
  └──────────────────────────────────────────────────────────┘
```

---

## Editions

| Edition | For | Billing |
|---------|-----|---------|
| Starter | Dev/test | Free + RU |
| Essential | Production AI/SaaS | RU (charged-by-query) |
| Premium | Enterprise | Capacity-based |
| Dedicated | Full control | Instance-based |

---

## Performance

- DDL on 14.1B rows: **5.53M rows/s** (5.5x improvement)
- P99/P999 latency: **~50% reduction** vs previous architecture
- TiCI: 1.6K QPS at P999=203ms on complex filters

---

## Key Ideas

- "Every AI agent deserves its own database — RU makes that real"
- "S3 is the new network" — storage backbone, not just backup
- "Context becomes data" — agent context needs ACID, not files
- Proven: Databricks (1M tables) → Atlassian (10M tables) → AI agents (millions of dynamic schemas)

---

## Links

- [Free trial](https://tidbcloud.com/free-trial/)
- [Essential 101](https://www.pingcap.com/essential101/)
- [TiDB Cloud AI](https://www.pingcap.com/ai)
- [Architecture docs](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/)
- [TiDB in 2025 — X](https://medium.com/@siddontang/tidb-in-2025-x-173f3510229c)
- [Context Becomes Data](https://medium.com/@siddontang/when-context-becomes-data-managing-ai-agent-context-with-tidb-307e667197bb)
- [Charged-by-Query](https://medium.com/@siddontang/the-power-of-charged-by-query-how-tidb-cloud-redefines-database-economics-for-the-ai-era-f5a3e76fcf1e)
- [Object Storage Playbook](https://medium.com/@siddontang/object-storage-is-rewriting-the-database-playbook-9e2dd1a81a53)
- [Every Agent Needs Its Own DB](https://medium.com/@siddontang/when-every-ai-agent-needs-its-own-database-why-tidb-cloud-is-the-answer-d3ff37580284)
- [TiDB for AIaaS](https://medium.com/@siddontang/why-tidb-is-the-best-database-for-ai-as-a-service-aiaas-08fe305489af)

---

## Install This Skill

```bash
mkdir -p ~/.openclaw/skills/tidb-x && curl -so ~/.openclaw/skills/tidb-x/SKILL.md https://raw.githubusercontent.com/siddontang/tidb-x-skill/main/SKILL.md
```
