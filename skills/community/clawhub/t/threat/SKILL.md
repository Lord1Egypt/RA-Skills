---
name: threat
description: Deep threat modeling workflow—system decomposition, trust boundaries, STRIDE-style threats, mitigations, prioritization, and tracking. Use when designing new features, reviewing architecture, or responding to security requirements (STRIDE, PASTA light).
---

# Threat Modeling (Deep Workflow)

Threat modeling turns **architecture** into **attack scenarios** and **mitigations** before code hardens incorrectly. It is **team-facing**—security is a **collaborative** exercise, not a gate at the end.

## When to Offer This Workflow

**Trigger conditions:**

- New service, major data flow change, public API, partner integration
- Compliance asks for “threat model” artifact
- Post-incident “how do we prevent class of issues”

**Initial offer:**

Use **six stages**: (1) scope & assets, (2) diagram & trust boundaries, (3) threats (STRIDE), (4) mitigations & controls, (5) prioritize & owners, (6) validate & iterate. Confirm **time box** (1–2 hour workshop vs async).

---

## Stage 1: Scope & Assets

**Goal:** Agree **what** we model and **what we protect**.

### Questions

1. **In scope**: apps, infra, data stores, admin tools, CI/CD?
2. **Crown jewels**: data (PII, keys), money, availability, reputation
3. **Adversaries**: script kiddies, malicious insiders, nation-state (usually pick **realistic** tiers)

### Output

**Scope paragraph** + **asset list** with sensitivity.

**Exit condition:** Shared understanding of **what hurts if lost**.

---

## Stage 2: Diagram & Trust Boundaries

**Goal:** Visual model with **boundaries** where trust changes.

### Practices

- **DFD-ish** diagram: external actors, services, data stores, queues
- Mark **trust boundaries**: internet boundary, partner VPC, employee laptop, CI system
- Note **auth** mechanisms crossing boundaries (mTLS, JWT, API keys)

### Pitfalls

- **Missing** CI/CD and admin paths—attackers love them
- **Over-detailed** diagram—keep level consistent

**Exit condition:** Diagram everyone in the room **recognizes** as their system.

---

## Stage 3: Threats (STRIDE)

**Goal:** Systematic **brainstorm**—not exhaustive fantasy.

### STRIDE prompts

- **Spoofing**: impersonation of user/service
- **Tampering**: data/code/config changed in transit or at rest
- **Repudiation**: actions not attributable—audit gaps
- **Information disclosure**: leaks to unauthorized
- **Denial of service**: resource exhaustion, dependency attacks
- **Elevation of privilege**: user becomes admin, lateral movement

### Technique

- Walk **each boundary** + **each asset** with STRIDE columns—**rapid ideation**, defer judgment
- Capture **threats** as short scenarios: “Attacker with leaked API key calls admin endpoint”

**Exit condition:** **Threat list** with **assumptions** stated (e.g., “requires MITM”).

---

## Stage 4: Mitigations & Controls

**Goal:** Map threats to **controls**—prevent, detect, respond.

### Control types

- **Prevent**: authZ checks, input validation, encryption
- **Detect**: logging, alerts, IDS, anomaly detection
- **Respond**: kill switches, incident playbooks

### Avoid

- **Control theater**—checkbox without real enforcement

**Exit condition:** Each **high** threat has at least one **planned** control or accepted risk with **owner**.

---

## Stage 5: Prioritize & Owners

**Goal:** **Ruthless** prioritization—fix what matters.

### Factors

- **Impact** × **likelihood** (even qualitative MoSCoW)
- **Ease of exploitation** vs **cost to fix**

### Tracking

- **Tickets** per mitigation; **link** to threat ID
- **Residual risk** explicitly accepted by appropriate authority when not fixed

**Exit condition:** **Roadmap** of mitigations with **dates**.

---

## Stage 6: Validate & Iterate

**Goal:** Model **ages**—revisit on major changes.

### Triggers for refresh

- New data flow, new integration, auth redesign
- **Pen test** findings that contradict assumptions

### Light validation

- **Red team** scenarios for top threats if mature org

---

## Final Review Checklist

- [ ] Assets and scope agreed
- [ ] Trust boundaries diagram current
- [ ] STRIDE pass completed for boundaries
- [ ] Mitigations mapped; owners assigned
- [ ] Residual risk explicit where unmitigated

## Tips for Effective Guidance

- **Facilitate**, don’t lecture—engineers own the system facts.
- Prefer **scenarios** over abstract “Tampering risk.”
- Link to **requirements** (“every admin action audited”) for traceability.

## Handling Deviations

- **No time workshop**: async diagram + STRIDE spreadsheet review.
- **Tiny feature**: **mini** threat model—still document **trust boundary** with external API.
