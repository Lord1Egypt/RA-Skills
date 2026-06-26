---
name: retro
description: Deep blameless postmortem workflow—timeline, impact, root cause vs contributing factors, what went well/poorly, action items with owners, and follow-through. Use after incidents, outages, or near-misses to improve reliability culture.
---

# Postmortems

A good postmortem **learns** without blaming individuals. It produces **owned actions** that reduce recurrence or improve detection—not generic “communicate better” platitudes.

## When to Offer This Workflow

**Trigger conditions:**

- SEV incidents, customer-visible outages, data-loss scares
- Near-misses worth documenting
- Need facilitation structure in a blame-prone culture

**Initial offer:**

Use **six stages**: (1) scope & audience, (2) timeline & impact, (3) root cause analysis, (4) what worked / didn’t, (5) action items, (6) communication & follow-up). Confirm internal-only vs customer-facing summary.

---

## Stage 1: Scope & Audience

**Goal:** Define readers (exec, engineering, CS) and redact PII or sensitive security details.

### Practices

- Blameless framing in the invite and template

**Exit condition:** Template chosen; owner for the final document.

---

## Stage 2: Timeline & Impact

**Goal:** Minute-resolution timeline in UTC: detection → onset → mitigation → resolution.

### Impact

- Users affected, duration, data integrity if relevant, SLA breach

**Exit condition:** Facts align with any external customer communication.

---

## Stage 3: Root Cause Analysis

**Goal:** Use five whys or fishbone as tools, not rituals. Separate **root cause** (fix that stops the class of failure) from **contributing factors** (process gaps, missing tests).

### Practices

- Do not name an individual as the “root cause”

**Exit condition:** Evidence-backed causal chain; contributing factors listed.

---

## Stage 4: What Worked / Didn’t

**Goal:** Reinforce positives (runbooks followed, clear comms) and negatives (missing dashboards, slow escalation).

---

## Stage 5: Action Items

**Goal:** Specific tickets with owners and dates; categorize prevent / detect / recover / process.

### Practices

- Avoid vague “add monitoring”—name metrics or signals

**Exit condition:** Items linked in the issue tracker.

---

## Stage 6: Communication & Follow-Up

**Goal:** Share summary internally; external postmortem only when policy requires; track completion in 30/60 days.

---

## Final Review Checklist

- [ ] Blameless tone; timeline and facts accurate
- [ ] Impact quantified where possible
- [ ] Root cause vs contributing factors distinguished
- [ ] Action items owned, dated, tracked
- [ ] Follow-up review scheduled

## Tips for Effective Guidance

- Match depth to severity; lightweight retro for minor incidents.
- Link traces, metrics, and logs in an appendix for engineers.
- Psychological safety enables honesty—leadership models it.

## Handling Deviations

- Security incidents: coordinate with legal/infosec before public detail.
