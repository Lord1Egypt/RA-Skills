---
name: tracing
description: Deep distributed tracing workflow—instrumentation boundaries, context propagation, sampling, tail-based analysis, service maps, and using traces for latency debugging. Use when adopting OpenTelemetry, debugging microservices, or tuning P99 latency.
---

# Distributed Tracing (Deep Workflow)

Traces answer **which hop** consumed time and **where** errors surfaced across services. Success requires **consistent propagation**, **meaningful spans**, and **sampling** that preserves signal without bankrupting storage.

## When to Offer This Workflow

**Trigger conditions:**

- Microservices “unknown latency” between A and B
- Adopting **OpenTelemetry**, Jaeger, Zipkin, X-Ray, Cloud Trace
- Need **service map** and **dependency** insights
- High cardinality or cost concerns from traces

**Initial offer:**

Use **six stages**: (1) define goals & SLOs, (2) instrumentation plan, (3) propagation & context, (4) sampling strategy, (5) analysis workflows, (6) governance & cost. Confirm **languages** and **infra** (K8s, service mesh).

---

## Stage 1: Goals & SLOs

**Goal:** Know **why** tracing exists—**latency**, **errors**, **dependency** discovery, or **customer** journey mapping.

### Questions

1. Top **p95/p99** pain routes?
2. **Compliance** or **PII** constraints on span attributes?
3. **Cardinality** tolerance—**user IDs** on every span?

**Exit condition:** **Success metrics**: e.g., “reduce unknown time in checkout to <5% of trace duration.”

---

## Stage 2: Instrumentation Plan

**Goal:** **Spanness** where it helps—**not** every function.

### Layers

- **HTTP server** middleware: span per request, **route** name normalized
- **HTTP clients**: outgoing spans with **peer** service
- **DB**: **client** spans with **statement** type—not raw SQL text in prod by default
- **Queues**: **produce/consume** spans with **message** correlation
- **Background jobs**: separate spans with **job** type

### Naming

- **Span names** stable (`GET /orders/{id}` patterns) vs high-cardinality raw paths

### Attributes

- **service.name**, **deployment.environment**, **http.status_code**, **db.system**—follow **semantic conventions** (OTel)

**Exit condition:** **Inventory** of frameworks auto-instrumented vs manual spans needed.

---

## Stage 3: Propagation & Context

**Goal:** **Trace ID** crosses async boundaries—**no broken traces**.

### Practices

- **W3C Trace Context** headers for HTTP; **messaging** propagators for Kafka/AMQP
- **Async** tasks: attach **context** when scheduling (executor, `asyncio`, `Promise`)
- **Batch** processing: **link** spans or **baggage** carefully—avoid leaking PII

### Service mesh

- **Sidecar** tracing vs library tracing—avoid **double** counting; configure one source of truth

**Exit condition:** **Broken trace rate** measurable; **top 5** causes documented (missing propagation, etc.).

---

## Stage 4: Sampling Strategy

**Goal:** **Representative** traces without **storing everything**.

### Head-based

- Fixed percentage; **always sample errors** (tail sampling often still needed)

### Tail-based

- **Interesting** traces (high latency, errors) retained—**complexity** but better signal

### Cost controls

- **Attribute** limits; **span** limits per trace; **drop** health checks

**Exit condition:** Written **policy**: baseline rate + **error** always + **latency** outliers.

---

## Stage 5: Analysis Workflows

**Goal:** Engineers **use** traces in incidents and perf work.

### Workflows

- **Trace view**: critical path, **longest** child span
- **Compare** releases: same route, different **p99** span
- **Service map** from edges—validate **unexpected** dependencies

### Anti-patterns

- **Only** looking at averages—**trace** is about **specific** slow requests

**Exit condition:** **Runbook** snippet: “How to find slowest span in checkout.”

---

## Stage 6: Governance & Cost

**Goal:** **PII** controlled; **budget** predictable.

### Practices

- **PII** redaction processors; **secrets** never in attributes
- **Retention** policies per env; **export** to cheap storage for long-term if needed
- **Ownership** of semantic conventions in org

---

## Final Review Checklist

- [ ] Instrumentation covers critical paths and async boundaries
- [ ] Propagation validated; broken trace rate monitored
- [ ] Sampling policy balances cost vs signal
- [ ] Semantic conventions applied consistently
- [ ] PII/secrets not in spans

## Tips for Effective Guidance

- Prefer **OpenTelemetry** as the **single** API with vendor exporters—avoid vendor lock-in at instrumentation.
- **DB spans**: recommend **query shape** (normalized) not raw SQL in prod.
- **Logs ↔ traces**: inject **trace_id** in logs for correlation.

## Handling Deviations

- **Monolith**: single-process traces still valuable—**async** and **thread** hops still break.
- **High cardinality** crisis: **drop** labels first, then sampling—**never** drop error visibility blindly.
