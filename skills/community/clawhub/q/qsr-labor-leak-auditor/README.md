# QSR Labor Leak Auditor
**v2.0.0 · McPherson AI · San Diego, CA**

AI-powered weekly labor cost auditor for QSR operators: tracks labor as a percentage of revenue, catches clock padding and scheduling drift, and flags mid-week risks before payroll closes.

**v2 update:** now uses contextual windows like catering, promotions, events, and weather before recommending labor cuts, with manager override and a full audit trail.

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

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license with an operational-use clarification.

See the [LICENSE](LICENSE) file for full details.

### Plain-English Summary

You are free to use, adapt, and share this skill for personal use and internal business operations.

You may not commercially redistribute it by reselling, repackaging, sublicensing, or offering it as a paid competing product without permission.

Operating this skill inside your own restaurant, franchise group, or business is allowed under this license clarification.

---

## Built By

**Blake McPherson**  
Founder, McPherson AI  
San Diego, CA

Builder of practical AI systems for restaurant operations, labor control, and execution discipline.

---

## Version

**v2.0.0**  
Adds contextual audit support, manager override logging, and weather-aware labor review.
