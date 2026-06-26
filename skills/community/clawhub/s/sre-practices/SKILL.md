---
name: sre-practices
description: Deep SRE workflow—SLOs/SLIs, error budgets, alerting, toil reduction, incident readiness, capacity, and balancing reliability with delivery. Use when improving production culture, defining service reliability targets, or reducing on-call pain.
---

# SRE Practices (Deep Workflow)

SRE is not “ops with a fancy title”—it is **engineering reliability** with **explicit trade-offs** between velocity and stability, measured with **SLOs** and managed through **error budgets** and **toil budgets**.

## When to Offer This Workflow

**Trigger conditions:**

- Defining or revisiting **SLOs**; too many pages or too few alerts
- “We need five nines” without user-visible meaning
- High **toil**: manual deploys, ticket-driven scaling, runbooks that never shrink
- Post-incident push for “more reliability” without cost discussion

**Initial offer:**

Walk through **six stages**: (1) user journeys & SLIs, (2) SLO targets & windows, (3) error budgets & policy, (4) alerting & on-call, (5) toil & automation, (6) continuous improvement. Confirm **service tiering** and **business criticality**.

---

## Stage 1: User Journeys & SLIs

**Goal:** Measure **what users actually experience**, not only server uptime.

### Activities

- List **critical journeys**: signup, pay, search, API sync, etc.
- For each, pick **SLI types**: availability, latency, freshness, correctness (where measurable)
- Define **SLI implementation**: e.g., “successful HTTP 2xx from LB / all requests excluding health checks” vs deeper **synthetic** probes

### Good SLIs

- **Specific**, **measurable**, **aligned** with pain—avoid vanity metrics

**Exit condition:** SLI definitions **documented** with data sources (metrics, logs, probes).

---

## Stage 2: SLO Targets & Windows

**Goal:** Set **achievable** targets with **explicit consequences**.

### Process

- Choose **window**: rolling 30d common; align with release cadence
- Set **target** (e.g., 99.9% availability) from **error budget** math: allowed downtime per month
- **Tier** services: not everything needs 99.99%

### Realism

- Account for **dependencies** you don’t control (public cloud, third-party APIs)—SLO cannot exceed dependency SLO unless architecture isolates failures.

**Exit condition:** Published **SLO document** per service or journey with **measurement method**.

---

## Stage 3: Error Budget Policy

**Goal:** Decide **how to spend** budget—feature velocity vs reliability work.

### Policy Examples

- Budget healthy → **ship** aggressively; budget low → **freeze** risky changes, focus on reliability
- **Exceptions** process: who can override, with what review

### Communication

- Product/engineering **shared ownership** of budget—not “SRE says no” in the dark

**Exit condition:** Written **policy**: what happens when budget burns at 25/50/100%.

---

## Stage 4: Alerting & On-Call

**Goal:** Pages are **symptom-based**, **actionable**, **low noise**.

### Principles

- Alert on **user pain** or **imminent SLO threat**, not every blip
- **Severity** maps to response: SEV1 customer-wide vs warning
- **Runbooks** linked; **ownership** clear

### On-Call Health

- **Limit pages** per engineer per week; track **toil hours**
- **Post-incident** follow-through to reduce repeat pages

**Exit condition:** Alert inventory reviewed; **tuning** backlog for noisy alerts.

---

## Stage 5: Toil & Automation

**Goal:** Reduce **manual, repetitive, automatable** work with **measurable** toil budgets.

### Identify Toil

- Frequent tickets, manual scaling, click-ops deploys, data fixes without guardrails

### Remediate

- **Eliminate** > **automate** > **document**—in that preference order when safe
- **Self-service** platforms with guardrails beat hero scripts

**Exit condition:** Toil reduction **roadmap** with owners; ideally **50%** toil cap aspiration per team norm (Google SRE guideline—adapt to org).

---

## Stage 6: Continuous Improvement

**Goal:** Reliability work is **prioritized** like features.

### Loops

- **Incident** → action items with tracking
- **Game days** / failure injection where mature
- **Quarterly** SLO review—targets drift with product changes

---

## Final Review Checklist

- [ ] SLIs tied to user-visible outcomes
- [ ] SLO targets realistic vs dependencies
- [ ] Error budget policy agreed with product
- [ ] Alerts actionable; noise tracked
- [ ] Toil identified with automation path

## Tips for Effective Guidance

- Translate **99.9%** to **minutes of downtime per month**—makes trade-offs concrete.
- Never promise **zero incidents**; promise **learning** and **measurable** improvement.
- Separate **SLI** (measurement) from **SLO** (target) from **SLA** (contract)—terms get confused.

## Handling Deviations

- **Early startup**: start with **basic monitoring + incident reviews** before full SLO program.
- **No SRE role**: practices still apply—relabel “production excellence” if needed.
