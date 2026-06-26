---
name: Vendor Performance Audit
version: 1.0.0
price: 29
category: productivity
author: Remy Claw
last_validated: 2026-03-03
tagline: Quarterly vendor review system with KPI scoring, improvement plans, and offboarding triggers.
---

# Vendor Performance Audit
**Framework: Vendor Performance Scorecard (VPS)**
**Output: Scored vendor review, improvement plan or offboarding recommendation**

Most vendor relationships drift because nobody's measuring them. This quarterly audit system gives you a structured way to evaluate every significant vendor, surface problems before they escalate, and make data-driven decisions about renewing, renegotiating, or replacing.

---

## When to Run This Audit

- **Quarterly** for all Priority vendors (ACV > $10K or operationally critical)
- **Semi-annually** for Standard vendors
- **Triggered** any time a major incident occurs (SLA breach, security issue, delivery failure)
- **Pre-renewal** (minimum 60 days before contract end)

---

## Phase 1: KPI Scorecard

Rate each dimension 1-5. Be honest — this is for your decision-making, not the vendor's feelings.

### Dimension 1: Delivery & SLA Performance (Weight: 30%)

| Score | Criteria |
|-------|---------|
| 5 | Consistently exceeds SLA. Proactive communication on any hiccup. Zero surprise failures. |
| 4 | Meets SLA >95% of the time. Issues are rare and resolved quickly. |
| 3 | Meets SLA most of the time. Occasional misses with reasonable resolution. |
| 2 | Frequent SLA misses. Resolution is slow or requires escalation. |
| 1 | Regular delivery failures. SLA is aspirational, not operational. |

**Evidence required:** Pull ticket data, delivery logs, or incident records. Don't score from memory.

### Dimension 2: Quality of Output (Weight: 25%)

| Score | Criteria |
|-------|---------|
| 5 | Output exceeds expectations. Error rate near zero. Rework is essentially unheard of. |
| 4 | Output meets quality bar consistently. Minor issues handled proactively. |
| 3 | Generally acceptable quality. Some rework required. |
| 2 | Quality is inconsistent. Rework is common. Internal team spends time fixing vendor output. |
| 1 | Output frequently doesn't meet standards. Significant internal overhead to compensate. |

### Dimension 3: Responsiveness & Communication (Weight: 20%)

| Score | Criteria |
|-------|---------|
| 5 | Always reachable. Proactively surfaces issues. Communication is clear and timely. |
| 4 | Responsive within agreed SLA. Communicates proactively most of the time. |
| 3 | Generally responsive but reactive. Sometimes requires chasing. |
| 2 | Slow to respond. You often initiate all communication. Escalations required. |
| 1 | Unreliable contact. Incidents discovered by you, not surfaced by them. |

### Dimension 4: Value vs. Cost (Weight: 15%)

| Score | Criteria |
|-------|---------|
| 5 | Clear ROI. Cost is at or below market for quality delivered. Strong value demonstrated. |
| 4 | Good value. Cost is reasonable given output and relationship quality. |
| 3 | Market rate. Neither a bargain nor obviously overpriced. |
| 2 | Starting to feel overpriced relative to value delivered or market alternatives. |
| 1 | Overpriced for what we get. Alternatives would deliver more for less. |

### Dimension 5: Strategic Alignment & Roadmap (Weight: 10%)

| Score | Criteria |
|-------|---------|
| 5 | Deeply aligned. They understand our business and proactively help us get where we're going. |
| 4 | Good alignment. They know our goals and adjust accordingly. |
| 3 | Transactional but functional. Delivers what's scoped, no more. |
| 2 | Misaligned in places. Their direction and ours are diverging. |
| 1 | No alignment. Product/service is moving away from our needs. |

---

## Phase 2: Composite Score & Tier Classification

**Weighted score calculation:**

```
VPS = (D1 × 0.30) + (D2 × 0.25) + (D3 × 0.20) + (D4 × 0.15) + (D5 × 0.10)
```

Max score = 5.0

| VPS Range | Tier | Recommended Action |
|-----------|------|-------------------|
| 4.0 – 5.0 | 🟢 Green — Trusted Partner | Renew, consider expanding scope or strategic partnership |
| 3.0 – 3.9 | 🟡 Yellow — Watch | Renew with conditions; issue improvement plan for lowest-scoring dimension |
| 2.0 – 2.9 | 🟠 Orange — At Risk | Renegotiate terms or begin sourcing alternatives; 60-day improvement window |
| 1.0 – 1.9 | 🔴 Red — Replace | Begin active replacement process; do not renew |

---

## Phase 3: Issue Log Review

Before finalizing the score, review your incident/ticket log for this vendor over the review period:

- How many incidents were opened? How many are still open?
- What was the average resolution time? Compare to SLA.
- Were any incidents flagged as critical/high-impact?
- Did any incidents result in downstream business impact (revenue loss, client complaints, compliance exposure)?

**Incident severity modifier:**
- 1+ critical incident with unresolved root cause → drop tier by one level
- 3+ medium incidents unresolved → flag for improvement plan regardless of VPS score

---

## Phase 4: Improvement Plan Template (Yellow & Orange Tiers)

If VPS < 4.0, issue a formal improvement plan:

**Improvement Plan — [Vendor Name] — [Quarter]**

- Review Period: [start] – [end]
- VPS Score: [X.X] / 5.0
- Tier: Yellow / Orange
- Review Date: [90 days from today]

**Key Issues Identified:**
1. [Specific issue with evidence]
2. [Specific issue with evidence]

**Required Improvements:**
1. [Specific, measurable change required] — Target: [metric] by [date]
2. [Specific, measurable change required] — Target: [metric] by [date]

**Consequences if not met:**
- Yellow: Move to Orange tier; begin parallel sourcing
- Orange: Contract not renewed; active replacement begins

**Acknowledgment:** Share this plan with the vendor. Get written acknowledgment.

---

## Phase 5: Offboarding Trigger Criteria

Initiate replacement when ANY of the following are true:
- VPS score < 2.0
- Two consecutive quarters in Orange tier
- Critical incident with material business impact and no credible root cause fix
- Vendor signals they are discontinuing the product/service
- Market alternative offers >30% better value at equivalent quality
- Compliance or security failure

When trigger is met: immediately move to replacement sourcing and set a hard cutover date.

---

## Audit Schedule Template

| Vendor | Category | ACV | Tier | Last Audit | Next Audit | Owner |
|--------|----------|-----|------|------------|------------|-------|
| [Name] | Software | $X | Green | [date] | [date] | [name] |

Run this as a quarterly review in your ops calendar.
