---
name: ui-roi-audit
description: Audit web pages and task-driven interfaces against source-cited conversion, usability, and ROI criteria.
license: MIT
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: "2.0"
---

# UI ROI Audit

Judge a web page or task-driven interface by whether it moves a person toward the conversion or task
the organization values, then rank fixes by likely return. Taste is out of scope. A sourced finding
needs a criterion ID; anything else must be labelled as the auditor's own observation and kept out
of the ranking.

## When to use

Use for “UI ROI audit”, “interface audit”, “usability ROI”, “ROI audit”, “conversion audit”, “audyt
ROI”, “audyt interfejsu”, “why does this page not convert?”, prioritizing interface fixes by
business impact, or justifying a design investment. Supported conversion pages: landing, home,
category, product, form, and checkout. Supported task-driven scope: one interface screen or task
flow with an observable success condition.

Do not use for copywriting, SEO, brand voice, WCAG compliance, or a revenue commitment. A browser
or screenshot helps but is optional; the workflow has no external dependency.

## Load on demand

| Situation | Load |
|---|---|
| A conversion-page type is known | Only that section of `references/page-type-criteria.md` |
| The conversion control is a form or checkout embedded in another page | Also load the matching form or checkout section |
| Auditing a conversion page or content that sells an action | `references/content-and-trust-criteria.md` |
| Estimating value or answering “is it worth it?” | `references/roi-model.md` |
| Auditing a task-driven interface, or the user requests usability | `references/usability-roi-module.md` |
| Before using a statistic or benchmark | `references/source-limitations.md` |
| Preparing the final report | `references/report-contract.md` |
| A format example is needed | `examples/sample-audit.md` |

Bibliography and reuse notes: `ATTRIBUTION.md`.

## Operating principles

- **Conversion before traffic.** A conversion gain applies to current and future traffic; paid
  traffic produces value only while it is bought (Loveday & Niehaus 2008, ch. 2).
- **Audit where money is lost.** Follow funnel drop-off rather than page prestige (ch. 3).
- **Evidence over taste.** Do not attach a source to an observation the criteria do not cover.
- **Conservative numbers.** Use ranges and explicit assumptions; never promise uplift.

## Required inputs

1. Target: URL, screenshot, pasted content, or task flow; one page, screen, or flow per run.
2. Type: landing, home, category, detail/product, form, checkout, or task-driven interface.
3. One success goal: purchase, lead, signup, call, completed task, time saved, or cost avoided.
4. Traffic source for a landing page: the ad or link that sends visitors there.
5. If available: monthly visits, conversion rate, average order/lead value, implementation cost,
   and funnel drop-off.

Ask for missing items 1–3 before auditing. Without item 5, continue qualitatively and never invent
numbers.

## Procedure

### 1. Frame

State target, type, goal, audience or users, traffic source when relevant, available data, and
observed viewport. If a target mixes types, name the primary type and any secondary criteria set.

**Output:** audit frame.

### 2. Inventory

Record the page or task flow in order: content, primary actions, navigation, inputs, feedback,
errors, recovery, and other observable states. For conversion pages, also capture value proposition,
images, price, and trust signals. Mark unavailable states as *not observed*.

**Output:** content inventory with viewport and observation limits.

### 3. Score content and page criteria

For conversion pages, load the relevant page-type section(s) and cross-cutting content criteria.
For a purely task-driven interface, skip this step and use the usability module in Step 4. Score
each applicable item:

| Score | Meaning |
|---|---|
| Pass | Present and doing its job |
| Partial | Present but weak, buried, or contradicted |
| Fail | Missing or working against the goal |
| N/A | Not applicable or not observable |

**Output:** scored criteria table; every Partial and Fail has page evidence.

### 4. Score usability when applicable

For a task-driven interface or requested usability review, load the usability module. When both
modules apply, keep usability findings separate from conversion-content findings.

**Output:** separate usability table, or a note that the module was not run.

### 5. Prioritize and estimate value

Rate each Partial and Fail High / Medium / Low on:

- **Exposure:** how much traffic meets it; first screen > later content > secondary state.
- **Severity:** how directly it blocks the conversion or task-success goal.
- **Effort:** work needed to fix it.

Rank high-exposure, high-severity, low-effort gaps first. For conversion pages, calculate value from
traffic, conversion rate, and order or lead value. For task interfaces, calculate cost avoided from
time, support, training, or rework using the usability module. Otherwise state “no data —
qualitative” and name the missing inputs.

**Output:** ranked top three with ROI range or qualitative status.

### 6. Report

Load `references/report-contract.md`, follow its output contract, citation rules, failure handling,
and final checklist.

**Output:** complete audit report.

## Anti-patterns

- Treating a general best practice as if either source stated it.
- Scoring an unobserved error, mobile, or post-submit state as a failure.
- Turning a scenario assumption into a benchmark or guaranteed uplift.
- Auditing an entire site or product when funnel or task data can identify the largest loss.
- Drafting replacement copy inside the audit; hand that work to a content-design workflow.

## Related skills

- `ux-content-design` — drafts copy after the audit.
- `kano-model-strategist` — decides whether a feature should exist.
- `socratic-dialogue` — stress-tests ROI assumptions.

## Framework credits

Built on Loveday & Niehaus (2008) and Marcus (2004). See `ATTRIBUTION.md` for the full bibliography,
verification notes, and reuse rules.
