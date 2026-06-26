# Trunkate AI: Optimization Examples & Benchmarks

This reference provides "Ground Truth" benchmarks for the Trunkate AI optimization pipeline. These examples demonstrate the semantic preservation hierarchy used by the `CompressorPipeline` when processing different input types.

## 1. Large Log Optimization (Diagnostic Data)

**Scenario**: Optimizing a massive build log to identify failure points while staying under a 500-token budget.

* **Input**: 4,500 Tokens (Raw `npm test` output with hundreds of passing lines).
* **Task**: "Extract the core failure reasons".
* **Result**: 210 Tokens.
* **ROI**: 95.3% reduction.

**Optimized Output Pattern**:

```text
[Trunkate Summary]
Failures detected in: auth-middleware.spec.ts
Error: Expected 200, received 401 (Unauthorized)
Context: symbolic_substitution applied to JWT_SECRET.
Status: All other 42 tests passed.
```

---

## 2. Conversation History Pruning (Proactive Mode)

**Scenario**: Automated `PreRequest` optimization when the `activator.py` detects history > 80% limit.

* **Input**: 120,000 Tokens (Multi-day coding session).
* **Target Budget**: 2,000 Tokens.
* **Optimization applied**: `intent_normalization` + `static_rewrite`.
* **ROI**: 98.3% reduction.

**Preservation Strategy**:

1. **Verbatim**: System instructions and the most recent 3 turns.
2. **Semantic**: Summarized mid-session logic (e.g., "Earlier discussed refactoring the Redis lifespan handler").
3. **Pruned**: Redundant `ls -R` outputs and intermediate `git status` checks.

---

## 3. Code Schema Compression (Database/SQL)

**Scenario**: Using `trunkate` to understand a massive database schema without ingesting 2,000 lines of SQL.

* **Input**: 1,800 Tokens (Full `schema.sql` export).
* **Task**: "Show the relationship between Users and API Keys".
* **Result**: 150 Tokens.
* **ROI**: 91.6% reduction.

**Optimized Output Pattern**:

```sql
-- Semantic Table Map
Table: api_keys_v2 (id: uuid, key: text, allocated_limit: int, email: text)
Relationship: api_keys_v2.email -> api_keys.email (One-to-Many)
```

---

## 4. Resilience Bypass (Error States)

**Scenario**: Handling service interruptions via `scripts/error_detector.py`.

* **Situation**: `HTTP 429: Account rate limit exceeded`.
* **Agent Behavior**: The `error_detector.py` issues a "Bypass" alert.
* **Outcome**: The agent proceeds with the **original history**.

**Internal Log Entry**:

```text
[TRK-20260228-FAIL] Category: rate_limit_bypass
Logged: 2026-02-28T18:40:00Z
Trigger: OnError (Rate Limit)
Action: No optimization attempted; raw history preserved.
```

---

*Note: Latency for these optimizations typically ranges from 150ms to 800ms depending on input size and tier allocation.*
