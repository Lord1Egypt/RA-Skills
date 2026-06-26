---
name: readme-authoring
description: Deep README workflow—audience, value proposition, quickstart, configuration, troubleshooting, contributing, and badges/links hygiene. Use when bootstrapping repos or improving onboarding for open source or internal libraries.
---

# README Authoring (Deep Workflow)

A README is the **front door** of a repository. Optimize for **time-to-first-success**: install, run, verify—then add depth for contributors and operators.

## When to Offer This Workflow

**Trigger conditions:**

- New repo; users cannot get running from docs alone
- Open-source release needing clear license and support expectations
- Internal library consumed by many teams

**Initial offer:**

Use **six stages**: (1) audience & promise, (2) above-the-fold, (3) quickstart, (4) configuration & operations, (5) contributing & governance, (6) maintenance). Confirm package ecosystem and license.

---

## Stage 1: Audience & Promise

**Goal:** First paragraph states **what** the project does, **for whom**, and **non-goals** if confusing.

**Exit condition:** Reader knows in 30 seconds if this repo matches their need.

---

## Stage 2: Above the Fold

**Goal:** Title, optional badges (CI, version, license), one screenshot or demo GIF if UI helps.

### Practices

- Link out to a full docs site when README would exceed ~300 lines

---

## Stage 3: Quickstart

**Goal:** Copy-paste commands that work on a clean machine; pin versions or point to release tags.

### Include

- Prerequisites (runtime, tools)
- Install and the **first** command with expected output shape

---

## Stage 4: Configuration & Operations

**Goal:** Environment variables table with defaults; ports; production notes (TLS, scaling, observability).

### Security

- Never document real secrets; reference secret stores and rotation

---

## Stage 5: Contributing & Governance

**Goal:** Link `CONTRIBUTING.md`, code of conduct, issue/PR templates; security disclosure policy for OSS.

---

## Stage 6: Maintenance

**Goal:** Changelog link or release notes; owning team; deprecation notices when relevant.

---

## Final Review Checklist

- [ ] Opening clarifies purpose and audience
- [ ] Quickstart verified on a fresh machine or CI
- [ ] Configuration and security expectations documented
- [ ] Contributing and license paths clear
- [ ] Maintenance signals (changelog, ownership) present

## Tips for Effective Guidance

- Run quickstart in CI (Docker or script) for critical OSS projects.
- Keep README skimmable; move deep dives to `docs/`.
- For libraries: link API reference and migration guides prominently.

## Handling Deviations

- **Monorepo:** root README as an index to packages with one-liner descriptions each.
