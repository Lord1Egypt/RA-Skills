---
description: "Security analysis for development plans and specifications — threat modeling, design-level vulnerability assessment, and spec change recommendations. No code required."
---

# Plan Security Analysis

Security review for development plans and specifications. Operates on architecture and design descriptions, not code. Produces threat models, design-level findings, and spec change recommendations.

## When to Use

- Before implementing a development plan
- When reviewing a feature specification
- During architecture design review
- As a section within the writing-plans workflow

## Inputs

The plan or specification document. Extract these from the text:

1. **Entry points** — every API endpoint, webhook, event handler, scheduled job
2. **Trust boundaries** — where data crosses between components, users, external services, databases
3. **Crown jewels** — credentials, PII, payment flows, automated actions, anything an attacker would target
4. **Auth model** — authentication strategy, session management, role/permission design, token strategy
5. **External integrations** — third-party APIs, service dependencies, auth methods, data exchanged
6. **Data flows** — end-to-end traces of critical data from entry to storage/action, noting where validation and sanitization occur

If the plan omits any of these, flag the gap as a finding.

## Analysis

### Phase 1: STRIDE per Trust Boundary

For EACH trust boundary extracted from the plan, systematically analyze all six categories:

| Category | Question |
|----------|----------|
| **Spoofing** | Can an attacker impersonate a legitimate entity at this boundary? (forged tokens, spoofed origins, replayed credentials) |
| **Tampering** | Can data crossing this boundary be modified? (MITM, parameter manipulation, unsigned payloads) |
| **Repudiation** | Can actions at this boundary be performed without audit trail? (missing logging, mutable logs, unsigned actions) |
| **Information Disclosure** | Can sensitive data leak across this boundary? (verbose errors, timing side-channels, unencrypted transit) |
| **Denial of Service** | Can this boundary be overwhelmed or blocked? (missing rate limits, resource exhaustion, queue flooding) |
| **Elevation of Privilege** | Can access controls at this boundary be bypassed? (privilege escalation, role confusion, token scope abuse) |

For each applicable threat:
- Describe the concrete attack scenario grounded in the planned architecture
- Reference specific components, endpoints, or data flows from the spec
- Rate as High/Medium/Low based on architectural evidence

### Phase 2: Attack Trees per Crown Jewel

For EACH crown jewel, build an attack tree:

```
Root: "Compromise [Crown Jewel Name]"
├── Path A: [Attack vector category]
│   ├── Step 1: [Specific technique] — Difficulty: [H/M/L], Detectability: [H/M/L]
│   ├── Step 2: [Next step in chain]
│   └── Prerequisites: [What attacker needs]
├── Path B: [Alternative attack vector]
│   └── ...
└── Path C: [Third vector if applicable]
    └── ...
```

Guidelines:
- Every leaf references a concrete component or endpoint from the spec
- Annotate each path with difficulty, detectability, prerequisites
- Include multi-step chains — real attacks combine weaknesses
- Prioritize paths by feasibility, not just theoretical possibility
- Mark paths that bypass multiple controls as "high priority"

### Phase 3: Business Logic Design Checklist

#### Race Conditions & Atomicity

For each state-changing operation described in the plan:

- Does the plan describe check-then-act patterns? Are they specified as atomic?
- Are counters, quotas, or rate limits described? Is atomicity specified?
- What locking/transaction strategy is specified for concurrent operations?
- For token refresh and nonce consumption — is the design atomic?
- What happens when two simultaneous requests hit the same state? (double-spend, double-submit, double-execute)

#### Pipeline & Decision Manipulation

For each data processing pipeline or automated decision described in the plan:

- Can crafted input manipulate extraction, template matching, or decisions?
- If the system learns patterns from input, can one user poison another user's data?
- If AI/ML is involved:
  - Can input override prompts? (prompt injection)
  - Can AI output bypass downstream validation?
  - Is AI response validated against an expected schema?
- Does the plan specify decision rules? Can they be gamed by manipulating input fields?
- Can processing results redirect output actions? (reply-to hijacking, recipient manipulation)
- Are pipeline stages idempotent? What happens on partial failure or retry?

#### Denial of Service & Cost Amplification

For each endpoint and integration described in the plan:

- Does any unauthenticated endpoint trigger N downstream operations? What is the amplification factor?
- Are paid resources (AI APIs, email, SMS) budget-gated BEFORE the call is made?
- Is there backpressure specified on task/job queues? Maximum queue depth?
- Can a single request cause unbounded database queries or writes?
- If one component fails, does it cascade to others?
- What is the cost ratio of an attacker request vs. defender operations?

### Phase 4: Risk Matrix

Map each identified threat to likelihood and impact:

| Threat ID | Description | Likelihood (1-5) | Impact (1-5) | Risk Score | Affected Crown Jewels |
|-----------|-------------|-------------------|--------------|------------|-----------------------|
| T-001 | ... | ... | ... | L x I | ... |

**Likelihood factors** (1=Unlikely, 5=Almost Certain):
- Attack complexity (steps, skill level)
- Required access (unauthenticated, authenticated, privileged)
- Availability of tools/exploits
- Detectability of the attack

**Impact factors** (1=Negligible, 5=Critical):
- Confidentiality: scope of data exposure
- Integrity: ability to modify data or behavior
- Availability: duration and scope of disruption
- Business: regulatory, reputational, financial consequences

## Output

Structure the output as:

```markdown
# Security Analysis — [Plan/Feature Name]

Date: [date] | Source: [plan document path]

## Executive Summary
[3-5 sentences: highest-risk threats, most exposed crown jewels, key architectural gaps]

## Extracted Architecture
### Entry Points
[Table: endpoint, auth requirement, input sources]

### Trust Boundaries
[List: boundary name, components on each side, data crossing]

### Crown Jewels
[List: asset, location, protection mechanism specified in plan]

### Data Flows
[For each critical flow: entry → processing → storage/action, noting validation points]

## STRIDE Analysis
[One subsection per trust boundary]

## Attack Trees
[One tree per crown jewel]

## Business Logic Concerns
### Race Conditions & Atomicity
[Findings]
### Pipeline & Decision Manipulation
[Findings]
### Denial of Service & Cost Amplification
[Findings]

## Risk Matrix
[Sorted by risk score descending]

## Spec Change Recommendations

### Critical (must address before implementation)
[Grouped by root cause]

### Important (address during implementation)
[Grouped by root cause]

### Suggested (defense-in-depth improvements)
[Grouped by root cause]

## Positive Observations
[What the plan already handles well — builds trust and prevents "everything is broken" fatigue]

## Gaps in Specification
[Architecture elements missing from the plan that prevent complete security analysis]
```

## What This Does NOT Cover

These require code and are handled by the full `/security-analyst` skill after implementation:

- Git history mining for vulnerability variants
- Dependency audit (npm audit, supply chain)
- Configuration and infrastructure review
- Exploit development with proof-of-concept code
- Code-level attack surface scanning
- Finding validation by adversarial critic
