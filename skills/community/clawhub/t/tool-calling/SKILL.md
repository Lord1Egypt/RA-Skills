---
name: tool-calling
description: Deep workflow for LLM tool/function calling—schema design, validation, permissions, errors, idempotency, testing, and safe orchestration with agents. Use when wiring models to APIs, databases, or internal tools.
---

# Tool Calling (Deep Workflow)

Tool calling is **contract design** between a **probabilistic** planner (the model) and **deterministic** systems. Failures are usually **schema**, **permissions**, or **ambiguity**—not the LLM “being dumb.”

## When to Offer This Workflow

**Trigger conditions:**

- Designing OpenAI/Anthropic-style **functions**, **MCP tools**, or internal JSON tool protocols
- Debugging wrong arguments, hallucinated parameters, or unsafe side effects
- Building agents with **many** tools—selection and routing problems

**Initial offer:**

Use **six stages**: (1) define tool surface, (2) schema & validation, (3) authz & safety, (4) execution semantics, (5) errors & observability, (6) evaluation & regression. Confirm **side-effect class** (read-only vs write).

---

## Stage 1: Define Tool Surface

**Goal:** **Minimize** tools; **maximize** clarity per tool.

### Principles

- **One action** per tool when possible—avoid mega-tools with mode flags unless necessary
- **Names** descriptive: `search_orders` not `do_stuff`
- **Prefer** idempotent operations where writes exist; separate **read** vs **write** clearly

### Anti-patterns

- Exposing **raw SQL** or **shell** to the model
- **Too many** overlapping tools → routing errors

**Exit condition:** Tool list with **purpose**, **inputs**, **outputs**, **side effects** table.

---

## Stage 2: Schema & Validation

**Goal:** Arguments are **typed**, **constrained**, and **machine-validated** before execution.

### Practices

- JSON Schema: **enums**, **min/max**, **patterns**, **required** fields
- **Normalize** dates, IDs, currencies server-side—**never** trust model formatting alone
- **Default** behaviors explicit in description + schema

### Descriptions

- Tool and parameter **docstrings** seen by model—**precise** language; **examples** of valid args

**Exit condition:** Validator rejects **invalid** args with **actionable** errors back to model or orchestrator.

---

## Stage 3: Authorization & Safety

**Goal:** Every tool call runs as **some principal** with **least privilege**.

### Patterns

- **User-scoped** credentials carried from session; tool implementation **re-checks** ownership (e.g., order_id belongs to user)
- **Admin tools** behind **explicit** allowlists and **human approval** when needed
- **Rate limits** per user + global circuit breakers

### Data exfiltration

- Tools that **read** sensitive data need **output filtering** and **logging** policies

**Exit condition:** **Threat brief**: “What if model is tricked into calling tool X?” answered.

---

## Stage 4: Execution Semantics

**Goal:** Clear **transactionality**, **retries**, and **idempotency**.

### Design

- **Idempotency keys** for writes; **dedupe** window
- **Timeouts** and **cancellation** propagation
- **Ordering**: parallel safe vs must be serial

### Long operations

- **Async** jobs with **poll** tool vs blocking calls—prefer **non-blocking** for UX and cost

**Exit condition:** Semantics documented for **retry** behavior (at-least-once delivery common).

---

## Stage 5: Errors & Observability

**Goal:** Model (or orchestrator) can **recover** from failures **without** leaking internals.

### Error messages

- **Structured** error codes: `ORDER_NOT_FOUND`, `PERMISSION_DENIED`
- **Hints** for model on how to fix—**without** stack traces to end users

### Observability

- **Trace IDs** across tool calls; **audit log** for write tools (who/when/args hash)

**Exit condition:** Dashboards/alerts on **tool error rate**, **latency**, **denials**.

---

## Stage 6: Evaluation & Regression

**Goal:** Tool changes are **tested** like APIs.

### Harness

- **Golden** conversations with expected tool calls (args normalized)
- **Adversarial** prompts attempting **privilege escalation**
- **Version** tools; **deprecate** with compatibility window

**Exit condition:** CI or manual **eval suite** before deploying new tools/schemas.

---

## Final Review Checklist

- [ ] Minimal orthogonal tool set
- [ ] Strict schema validation on server
- [ ] AuthZ enforced per call; sensitive reads controlled
- [ ] Idempotency and timeouts defined for writes
- [ ] Structured errors + observability + eval harness

## Tips for Effective Guidance

- Treat tool descriptions as **API docs the model reads**—iterate wording like UX copy.
- Recommend **two-step** patterns for dangerous ops: propose → confirm (human or policy).
- When using **MCP**, same discipline—**server** must validate everything.

## Handling Deviations

- **Read-only RAG**: fewer semantic risks—still validate query args and **injection** into search backends.
- **Local tools** (filesystem): **sandbox**, **path allowlists**, **size limits**.
