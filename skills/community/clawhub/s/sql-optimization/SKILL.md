---
name: sql-optimization
description: Deep SQL performance workflow—symptom framing, execution plans, indexing strategy, query rewrite, locking/transaction behavior, statistics, partitioning, and verification. Use when queries time out, DB CPU spikes, or migrations change access patterns.
---

# SQL Optimization (Deep Workflow)

Optimization without measurement is guesswork. Structure the work as **observe → explain (plan) → change → verify**, with explicit attention to **correctness**, **locks**, and **write amplification** from indexes.

## When to Offer This Workflow

**Trigger conditions:**

- Slow queries, growing P95/P99, replication lag, lock waits
- ORM-generated SQL surprises; N+1 at DB layer
- Index explosion, bloat, or “we added indexes everywhere”

**Initial offer:**

Use **six stages**: (1) frame the problem, (2) reproduce & measure, (3) read execution plans, (4) schema & indexes, (5) query & transaction tuning, (6) verify & guardrail. Confirm **engine** (PostgreSQL, MySQL, SQL Server, etc.) and **environment** (prod-like data volume).

---

## Stage 1: Frame the Problem

**Goal:** Define **SLO**, **scope**, and **non-goals**.

### Questions

1. Which **queries** or **endpoints** are slow? User-facing vs batch?
2. **Regression**—did deploy, data volume, or stats change?
3. **Isolation level** and **consistency** requirements—can we read replicas?
4. **Write risk**: is this table write-heavy? Index cost?

**Exit condition:** One-line **problem statement** with metric (e.g., “p95 2.4s on `/reports` at 10k RPS”).

---

## Stage 2: Reproduce & Measure

**Goal:** **Stable repro** with representative **cardinality** and **parameters**.

### Actions

- Capture **exact SQL**, parameters, and **frequency**
- Use **EXPLAIN (ANALYZE, BUFFERS)** or equivalent—engine-specific
- Check **buffer cache** effects: cold vs warm cache; run twice when needed
- Compare **prod stats** vs staging—row counts, histograms

### Pitfalls

- Optimizing on empty dev DB
- Different **parameter sniffing** values changing plan choice

**Exit condition:** Baseline numbers + **plan hash** or saved plan for A/B.

---

## Stage 3: Read Execution Plans

**Goal:** Name the **dominant cost**: seq scan, bad join order, sort, hash spill, nested loop explosion.

### Interpret (adapt to engine)

- **Seq scan** on large tables—filter selectivity? missing index? stats?
- **Index scan** vs **bitmap** vs **index only**—covering indexes trade-offs
- **Joins**: wrong order, missing stats, outdated NDV
- **Sort/hash** spills to disk—work_mem / memory grants
- **Locks**: `FOR UPDATE`, long transactions, hot row updates

**Exit condition:** Hypothesis tied to **plan node(s)**, not generic “add index.”

---

## Stage 4: Schema & Indexes

**Goal:** **Right indexes** for read paths without destroying writes.

### Strategy

- **Composite index column order**: equality → range; avoid redundant indexes
- **Partial indexes** for hot subsets
- **Covering** indexes vs table bloat—measure write cost
- **Foreign keys** and **constraints** affecting plans
- **Statistics**: `ANALYZE`, extended stats, histograms—when stale stats lie

### Advanced (when relevant)

- **Partitioning** for prune + maintenance
- **Materialized views** / pre-aggregation for heavy reports

**Exit condition:** DDL proposal with **rationale** and **rollback** (drop index concurrently if supported).

---

## Stage 5: Query & Transaction Tuning

**Goal:** Sometimes the fix is **SQL rewrite**, not hardware.

### Techniques

- Reduce **rows touched** early (CTEs vs inline—engine-dependent)
- **Pagination** without OFFSET on huge pages (keyset)
- **Batch** vs row-by-row; **UNION ALL** vs OR
- **N+1**: batch queries, joins, data loader patterns
- **Transactions**: shorten locks; avoid unnecessary `SELECT FOR UPDATE`
- **ORM**: eager vs lazy loading discipline

**Exit condition:** New plan shows lower cost / measured latency; **lock time** acceptable.

---

## Stage 6: Verify & Guardrail

**Goal:** Improvement **holds** under load and doesn’t regress neighbors.

### Verify

- Re-run **EXPLAIN ANALYZE** with production-like parameters
- Load test or shadow traffic if available
- **Monitor**: buffer hit ratio, index bloat, replication lag

### Guardrails

- **Query timeouts** and **statement_timeout** where safe
- **Alerts** on sequential scans on large tables if observability supports

---

## Final Review Checklist

- [ ] Baseline and target metrics documented
- [ ] Plan-based root cause, not guesswork
- [ ] Index/DDL changes justified vs write load
- [ ] Transaction/lock behavior considered
- [ ] Verification on realistic data and load

## Tips for Effective Guidance

- Always mention **parameter sniffing** and **stale statistics** as frequent culprits.
- Warn when **adding indexes** on very write-heavy tables without measuring bloat.
- Prefer **keyset pagination** education for large lists.

## Handling Deviations

- **No EXPLAIN access**: infer from symptoms + ORM logs + index list; recommend safe staging repro.
- **Vendor DB**: name that **hints** and features differ—avoid PostgreSQL-only advice on SQL Server without caveat.
