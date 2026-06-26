---
name: system-design
description: Deep system design workflow—requirements, capacity, APIs, data, consistency, failure modes, trade-offs, and evolution. Use when preparing interviews, RFCs, greenfield systems, or major redesigns (microservices, multi-region, real-time).
---

# System Design (Deep Workflow)

System design is **structured decision-making** under constraints. The output is not a diagram—it is **clarity on requirements**, **explicit trade-offs**, and a **path to evolve** when load and features change.

## When to Offer This Workflow

**Trigger conditions:**

- “Design Twitter/Instagram/WhatsApp” (interview style)
- Greenfield service, major scale milestone, multi-region, or realtime needs
- Refactoring monolith—**boundaries** and **data ownership** questions

**Initial offer:**

Use **seven stages**: (1) clarify requirements, (2) capacity & SLO sketch, (3) high-level architecture, (4) data model & storage, (5) APIs & traffic patterns, (6) reliability & failure modes, (7) trade-offs & evolution. Ask **interview mode** (time-boxed) vs **real project** (depth).

---

## Stage 1: Clarify Requirements

**Goal:** **Functional** and **non-functional** requirements explicit.

### Functional

- Core **user actions**; **read vs write** ratio; **search**, **ranking**, **notifications**?

### Non-functional

- **Scale**: DAU, QPS, data size, growth—orders of magnitude OK if unknown
- **Latency**: p95/p99 targets; sync vs async acceptable?
- **Consistency**: can reads be stale? global ordering needed?
- **Durability**: loss tolerance; audit; compliance

### Out of Scope

- Explicitly list **non-goals** to prevent scope creep in interviews and real life

**Exit condition:** **Problem statement** one paragraph; **constraints** bullet list.

---

## Stage 2: Capacity & SLO Sketch

**Goal:** **Back-of-envelope** math to sanity-check bottlenecks.

### Rough math

- Requests/day → QPS peak with **3–10×** factor if needed
- Storage/day; **replication** multiplier
- **Bandwidth** for large payloads (images, video)

### SLO mindset

- **Availability** vs **cost**; **strong consistency** vs **latency**

**Exit condition:** Identified **likely bottleneck** class: DB, network, fan-out, storage.

---

## Stage 3: High-Level Architecture

**Goal:** Boxes and arrows with **reasons**.

### Typical layers

- **Clients** → **LB/API** → **services** → **caches/queues** → **databases/object storage**
- **CDN** for static and cacheable API responses when applicable
- **Async** processing for heavy work (indexing, emails, ML)

### Principles

- **Separation** of read/write (CQRS) only when justified by scale
- **Idempotent** workers; **at-least-once** messaging assumptions

**Exit condition:** Diagram + **why not simpler** (monolith) answered in one paragraph.

---

## Stage 4: Data Model & Storage

**Goal:** Choose **stores** for access patterns, not buzzwords.

### Questions

- **Relational** vs **document** vs **wide-column** vs **graph**—**query patterns** first
- **Sharding** key if huge scale; **hot partitions** risk
- **Caching**: what, TTL, invalidation
- **Search**: inverted index service (Elasticsearch, etc.) vs DB full-text

### Consistency

- **Transactions** boundaries; **sagas** for cross-service consistency; **eventual** where OK

**Exit condition:** **Schema sketch** or entity list; **read/write paths** for top 3 operations.

---

## Stage 5: APIs & Traffic Patterns

**Goal:** **Interface** design and **operational** behavior.

### REST vs RPC vs GraphQL

- Trade-offs: **coupling**, **overfetching**, **caching**, **team boundaries**

### Realtime

- **WebSockets/SSE**; **presence**; **ordering**; **backpressure**

### Rate limiting & auth

- **Gateway** enforcement; **user** vs **service** identity

**Exit condition:** Example **APIs** or **events** for core flows; **pagination** strategy.

---

## Stage 6: Reliability & Failure Modes

**Goal:** **Failure is normal**—design **degradation**.

### Consider

- **Retries** with backoff; **timeouts** everywhere; **circuit breakers**
- **Partial outages**: read-only mode, stale cache, queue backlog
- **Disaster**: **backup/restore**, **multi-region** (active-active vs DR)

### Observability

- **Metrics, logs, traces**; **SLOs** for critical paths

**Exit condition:** **Top 5 failure scenarios** + **mitigation** each.

---

## Stage 7: Trade-offs & Evolution

**Goal:** Show **maturity**—v1 vs v2 path.

### Articulate

- What you build **first** vs later; **feature flags**; **strangler** patterns
- **Interview**: summarize **bottleneck** and **future scaling** in 60 seconds

---

## Final Review Checklist

- [ ] Requirements and non-goals clear
- [ ] Rough capacity points to bottleneck
- [ ] Architecture justified vs simpler alternatives
- [ ] Data stores match access patterns + consistency needs
- [ ] APIs/events and failure modes addressed
- [ ] Evolution path stated

## Tips for Effective Guidance

- **Interview**: time-box **depth**—breadth first, then zoom one area on request.
- Always mention **hot keys**, **fan-out**, and **backpressure** for scale.
- Distinguish **exactly-once** myth—usually **at-least-once** + idempotency.

## Handling Deviations

- **Small system**: still run stages **lightly**—habit prevents over-engineering later.
- **Existing system**: focus on **incremental** changes and **data migration** risks.
