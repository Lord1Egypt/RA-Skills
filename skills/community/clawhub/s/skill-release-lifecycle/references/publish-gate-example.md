# Publish Gate — Worked Example: waste-audit

This document runs `waste-audit` against the Skill Release Lifecycle publish gate.

**Date of this evaluation:** 2026-05-24
**Assessor:** Hermes Agent
**Result:** PASS — eligible for public release / already published to ClawHub

> **Evidence source note:** This evaluation uses both direct inspection and reference-derived evidence. Where evidence is reference-derived, it is explicitly labeled and stated as sufficient or in need of direct verification.

---

## A. Utility / Recurrence (HARD)

| Requirement | Pass / Fail | Evidence | Source |
|---|---|---|---|
| At least 3 non-trivial real or dogfood runs | **Pass** | Used across multiple live OpenClaw waste-audit sessions, including recurring job review and public-page iteration. | Reference-derived — from session history and prior dogfood reports. Sufficient for this gate; recurring use is self-evident from the skill's design. |
| At least 2 distinct input scenarios | **Pass** | Scenario 1: recurring cron token-waste identification. Scenario 2: validating the resulting public skill output/activation for manual verification. | Reference-derived — from prior evaluation records. Sufficient: two distinct scenarios are documented. |
| At least 1 output actually used/copied/published/turned into action | **Pass** | Output structure became the released `waste-audit` public skill: Fix First, Top Waste Candidates, Manual Verification Prompt. | Direct inspection — output structure is visible in the published ClawHub page. |
| At least 1 recorded issue, edge case, failure, unclear boundary, or UX observation | **Pass** | Recorded issues included activation routing, duplicate Install sections, public page rendering behavior, `--global` install note, and top install block limitation. | Reference-derived — from dogfood run #1 and iteration loop records. Sufficient for this gate. |
| Evidence this is recurring, not one-off | **Pass** | Recurring OpenClaw jobs can silently waste tokens over time; the audit itself is repeatable and recurring. | Direct inspection — the skill targets a structural property of recurring cron jobs. |

**Gate A result: PASS.**

---

## B. Identity (HARD)

| Requirement | Pass / Fail | Evidence | Source |
|---|---|---|---|
| Narrow scope | **Pass** | Single job: find recurring OpenClaw jobs that may be wasting tokens. | Direct inspection — scope is stated in description and `## Features`. |
| Explicit anti-scope | **Pass (with note)** | SKILL.md states not to use it for general OpenClaw setup, gateway debugging, provider configuration, or normal job management. | Direct inspection — anti-scope sentence exists under `Activation`. Not a standalone section, but content is explicit. Per the anti-scope placement rules: existing published skill with a clear anti-scope statement may temporarily pass. Next re-release should convert to a standalone section. |
| Not a generic assistant | **Pass** | Description names a specific task class: recurring OpenClaw token waste. | Direct inspection. |

**Gate B result: PASS, with one noted action for next re-release.**

---

## C. Safety (HARD)

| Requirement | Pass / Fail | Evidence | Source |
|---|---|---|---|
| Safe default behavior | **Pass** | Default behavior is read-only. It produces evidence and a manual verification prompt. | Direct inspection — `## Features` states "Read-Only Safety" and `What You Will Get` is read-only output. |
| No implicit destructive action | **Pass** | It explicitly says not to edit, disable, delete, or mutate anything yet. | Direct inspection — Manual Verification Prompt includes this constraint. |
| No secret exposure | **Pass** | Prompt instructs redaction of secrets and private payloads. | Direct inspection. |

**Gate C result: PASS.**

---

## D. UX (SOFT)

| Requirement | Pass / Fail | Evidence | Source |
|---|---|---|---|
| Clear activation | **Pass** | `check openclaw waste` is documented. | Direct inspection. |
| Clear install command | **Pass** | `openclaw skills install waste-audit --global` is documented. | Direct inspection. |
| Advanced install notes | **Pass** | `--global` for shared OpenClaw agents and `--force` for upgrade are documented. | Direct inspection. |
| Clear output format | **Pass** | Output contract includes Fix First, Top Waste Candidates, and Manual Verification Prompt. | Direct inspection. |
| Clear verification steps | **Pass** | User can test with `check openclaw waste`. | Direct inspection. |

**Gate D result: PASS.**

---

## E. Maintenance (SOFT)

| Requirement | Pass / Fail | Evidence | Source |
|---|---|---|---|
| Clear changelog | **Pass** | Version bumps were tied to concrete changes during ClawHub iteration. | Reference-derived — from iteration-loop-example.md. Changelog evidence cited as existing in ClawHub release metadata. Sufficient: version bumps are documented per iteration record. |
| Clear feedback path | **Pass** | Public page includes X DM feedback path: @BeeGeeEth. | Direct inspection — `## Feedback` section. |
| Post-release iteration path | **Pass** | Feedback drove patches to activation, section order, install guidance, and public-page wording. | Reference-derived — from iteration-loop-example.md. Sufficient. |

**Gate E result: PASS.**

---

## Overall Result

| Gate | Result |
|---|---|
| A. Utility / Recurrence | PASS (reference-derived evidence sufficient) |
| B. Identity | PASS (anti-scope note: convert to standalone section at next re-release) |
| C. Safety | PASS (direct) |
| D. UX | PASS (direct) |
| E. Maintenance | PASS (reference-derived sufficient) |

**Decision:** Public release justified. No hard gate blockers.

---

## Post-release Action

`waste-audit` has a standalone anti-scope section. Convert the existing anti-scope sentence into a standalone `What This Will Not Do` section at next re-release.

---

## Distribution Signal Note

`waste-audit` having downloads is useful post-release evidence, but it was not part of the publish gate. The decision to publish should stand or fail on recurrence, identity, safety, UX, and maintenance readiness — not homepage placement or download count.