# QSR Labor Leak Auditor
**v3.1.5 · McPherson AI · San Diego, CA**

AI-powered weekly labor cost auditor for QSR operators: tracks labor as a percentage of revenue, catches clock padding and scheduling drift, and flags mid-week risks before payroll closes.

**v2 update:** now uses contextual windows like catering, promotions, events, and weather before recommending labor cuts, with manager override and a full audit trail.

## Observa Edge Basic Beta

Observa Edge Basic Beta is a separate, optional OpenClaw plugin from McPherson AI for local guardrails on covered tool routes. Installing this restaurant skill leaves Guard inactive. Accountless Shadow previews covered requests locally. Guard enrollment is restricted and requires approval and a separate local owner activation.

[**Explore Observa Edge Basic Beta →**](https://mcphersonai.com/observa/edge-basic?utm_source=github&utm_medium=skill-readme&utm_campaign=observa-edge-basic-beta&utm_content=qsr-labor-leak-auditor)

*Publisher notice. The QSR skill’s behavior and data handling are unchanged.*

---

## Overview

QSR Labor Leak Auditor is a weekly labor monitoring skill built for restaurant operators who need tighter control over labor cost before payroll is locked in.

It is designed to help managers identify labor inefficiency early in the week, not after the damage is already done.

This skill reviews labor performance in context and highlights the most likely causes of drift, overstaffing, and avoidable wage leakage so store leadership can take corrective action while there is still time to act.

It is built from real operating experience inside high-volume QSR environments.

---

## What It Does

QSR Labor Leak Auditor functions as an operational labor cost watchdog for store leadership.

It helps operators:

- Track labor as a percentage of revenue by day
- Catch mid-week labor drift before payroll closes
- Identify possible clock padding and scheduling inefficiency
- Flag overstaffing relative to sales performance
- Distinguish normal labor pressure from avoidable waste
- Surface patterns that managers may miss during busy weeks
- Recommend corrective action before the week ends

Rather than simply reporting numbers, this skill is designed to think like an experienced QSR operator reviewing the labor story behind the metrics.

---

## Core Use Cases

### 1. Daily Labor-to-Sales Tracking
Monitors labor performance against revenue trends across the week to identify when the store is falling out of alignment.

### 2. Mid-Week Risk Detection
Provides an actionable warning while the operator still has time to reduce unnecessary hours, rebalance staffing, or tighten shift execution.

### 3. Clock Padding and Labor Leak Review
Flags patterns that may suggest idle labor, weak deployment, long overlaps, or unnecessary scheduled coverage.

### 4. Scheduling Drift Analysis
Detects when staffing patterns begin to separate from actual business volume, creating preventable labor loss.

### 5. Contextual Audit Support
Evaluates labor pressure with awareness that not every spike is a true problem. Weather, events, promos, catering, or unusual traffic may explain temporary variance.

### 6. Manager Override Logging
Supports operator judgment by allowing exceptions and context to be acknowledged rather than forcing blind labor cuts.

---

## Who It’s For

QSR Labor Leak Auditor is intended for:

- General Managers
- Assistant Managers
- Franchise Operators
- District Managers
- Multi-unit leaders
- Builders creating QSR labor intelligence systems

---

## Why It Exists

Most labor reports tell you what happened after the week is already over.

QSR Labor Leak Auditor is built to help operators intervene before payroll closes.

The goal is simple:

**catch labor waste early, protect margins, and improve labor discipline without losing operational context.**

---

## Example Outcomes

Used consistently, this type of system can help teams:

- Catch labor overruns before the end of the week
- Reduce avoidable wage leakage
- Improve staffing discipline
- Surface possible clock padding or poor deployment patterns
- Create better mid-week decision-making
- Improve accountability around labor performance

---

## Positioning

QSR Labor Leak Auditor is part of the broader McPherson AI QSR operations ecosystem.

It fits alongside skills focused on:

- daily ops control
- store-level diagnostics
- district visibility
- execution discipline
- operational accountability

---

## Technical Infrastructure

- **Logic:** AI-assisted development
- **Deployment:** DigitalOcean VPS
- **Connectivity:** Private Tailscale Mesh
- **Security:** Fail2Ban intrusion prevention

---

## License

McPherson AI distributes this ClawHub edition under MIT-0. The GitHub source edition is available under Apache License 2.0. See [LICENSE](LICENSE). Third-party materials remain subject to their applicable terms.

---

## Built By

**Blake McPherson**  
Founder, McPherson AI  
San Diego, CA

Builder of practical AI systems for restaurant operations, labor control, and execution discipline.

---

## Version

**v3.1.4**
Publisher-notice refresh: Observa CTA updated to the current Getting Started flow. No functional changes.

**v3.1.3**
Publisher-note release; the Observa private beta is now open. No functional changes.

**v3.1.2**
Publisher-note release; operational behavior and license unchanged.

**v2.0.0**  
Adds contextual audit support, manager override logging, and weather-aware labor review.
