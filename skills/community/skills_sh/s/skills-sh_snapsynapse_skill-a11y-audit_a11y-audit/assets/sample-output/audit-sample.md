# Accessibility Audit Report

## Header

| Field | Value |
|---|---|
| Project | sam-rogers.com |
| Date | 2026-03-26 |
| Standards | WCAG 2.1 AA |
| Tool Version | axe-core (via scan.js); report.js v1 |
| URL | https://sam-rogers.com |

## Executive Summary

sam-rogers.com was audited across 15 page(s). Automated scanning found **33 issue instance(s)** across **7 rule(s)**.

| Impact | Instances |
|---|---|
| serious | 5 |
| moderate | 28 |

Lighthouse was skipped: Lighthouse disabled for this run.

## Automated Scan Results

### Pages Scanned

- https://sam-rogers.com/about/
- https://sam-rogers.com/archive/
- https://sam-rogers.com/blog/
- https://sam-rogers.com/contact/
- https://sam-rogers.com/now/
- https://sam-rogers.com/privacy/
- https://sam-rogers.com/projects/
- https://sam-rogers.com/tags/
- https://sam-rogers.com/blog/substack/
- https://sam-rogers.com/blog/fringer/
- https://sam-rogers.com/now/2022-11/
- https://sam-rogers.com/now/2021-11/
- https://sam-rogers.com/about/bio/
- https://sam-rogers.com/about/colophon/
- https://sam-rogers.com/

### Findings by Rule

| Rule | Impact | Instances | Pages | WCAG |
|---|---|---|---|---|
| [landmark-unique](https://dequeuniversity.com/rules/axe/4.11/landmark-unique?application=axeAPI) | moderate | 15 | 15 | - |
| [region](https://dequeuniversity.com/rules/axe/4.11/region?application=axeAPI) | moderate | 8 | 8 | - |
| [landmark-one-main](https://dequeuniversity.com/rules/axe/4.11/landmark-one-main?application=axeAPI) | moderate | 2 | 2 | - |
| [heading-order](https://dequeuniversity.com/rules/axe/4.11/heading-order?application=axeAPI) | moderate | 2 | 2 | - |
| [page-has-heading-one](https://dequeuniversity.com/rules/axe/4.11/page-has-heading-one?application=axeAPI) | moderate | 1 | 1 | - |
| [frame-title](https://dequeuniversity.com/rules/axe/4.11/frame-title?application=axeAPI) | serious | 1 | 1 | SC 4.1.2 |
| [list](https://dequeuniversity.com/rules/axe/4.11/list?application=axeAPI) | serious | 4 | 4 | SC 1.3.1 |

### Quick Fixes

- **list** (serious, 4 instances): Ensure `<li>` elements are direct children of `<ul>` or `<ol>`. Do not place non-list content directly inside list containers.
- **region** (moderate, 8 instances): Ensure all page content is inside a landmark region (`<main>`, `<nav>`, `<header>`, `<footer>`, or `role="..."`).
- **landmark-one-main** (moderate, 2 instances): Wrap the primary content area in a `<main>` element. This also resolves most `region` violations.
- **heading-order** (moderate, 2 instances): Heading levels should increase by one (h1 → h2 → h3). Do not skip levels.

## WCAG 2.1 AA Compliance Matrix

> This is an automation-assisted status view, not a conformance certification.

| SC | Name | Level | Status |
|---|---|---|---|
| **Perceivable** | | | |
| SC 1.1.1 | Non-text Content | A | Pass |
| SC 1.2.1 | Audio-only and Video-only (Prerecorded) | A | Manual |
| SC 1.2.2 | Captions (Prerecorded) | A | N/A |
| SC 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | Manual |
| SC 1.2.4 | Captions (Live) | AA | Manual |
| SC 1.2.5 | Audio Description (Prerecorded) | AA | Manual |
| SC 1.3.1 | Info and Relationships | A | **Fail** |
| SC 1.3.2 | Meaningful Sequence | A | Manual |
| SC 1.3.3 | Sensory Characteristics | A | Manual |
| SC 1.3.4 | Orientation | AA | Manual |
| SC 1.3.5 | Identify Input Purpose | AA | N/A |
| SC 1.4.1 | Use of Color | A | Pass |
| SC 1.4.2 | Audio Control | A | N/A |
| SC 1.4.3 | Contrast (Minimum) | AA | Pass |
| SC 1.4.4 | Resize Text | AA | Pass |
| SC 1.4.5 | Images of Text | AA | Manual |
| SC 1.4.10 | Reflow | AA | Manual |
| SC 1.4.11 | Non-text Contrast | AA | Manual |
| SC 1.4.12 | Text Spacing | AA | Pass |
| SC 1.4.13 | Content on Hover or Focus | AA | Manual |
| **Operable** | | | |
| SC 2.1.1 | Keyboard | A | N/A |
| SC 2.1.2 | No Keyboard Trap | A | Manual |
| SC 2.1.4 | Character Key Shortcuts | A | Manual |
| SC 2.2.1 | Timing Adjustable | A | N/A |
| SC 2.2.2 | Pause, Stop, Hide | A | N/A |
| SC 2.3.1 | Three Flashes or Below Threshold | A | Manual |
| SC 2.4.1 | Bypass Blocks | A | Pass |
| SC 2.4.2 | Page Titled | A | Pass |
| SC 2.4.3 | Focus Order | A | Manual |
| SC 2.4.4 | Link Purpose (In Context) | A | Pass |
| SC 2.4.5 | Multiple Ways | AA | Manual |
| SC 2.4.6 | Headings and Labels | AA | Manual |
| SC 2.4.7 | Focus Visible | AA | Manual |
| SC 2.5.1 | Pointer Gestures | A | Manual |
| SC 2.5.2 | Pointer Cancellation | A | Manual |
| SC 2.5.3 | Label in Name | A | Manual |
| SC 2.5.4 | Motion Actuation | A | Manual |
| **Understandable** | | | |
| SC 3.1.1 | Language of Page | A | Pass |
| SC 3.1.2 | Language of Parts | AA | N/A |
| SC 3.2.1 | On Focus | A | Manual |
| SC 3.2.2 | On Input | A | Manual |
| SC 3.2.3 | Consistent Navigation | AA | Manual |
| SC 3.2.4 | Consistent Identification | AA | Manual |
| SC 3.3.1 | Error Identification | A | Manual |
| SC 3.3.2 | Labels or Instructions | A | Pass |
| SC 3.3.3 | Error Suggestion | AA | Manual |
| SC 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | Manual |
| **Robust** | | | |
| SC 4.1.1 | Parsing | A | Manual |
| SC 4.1.2 | Name, Role, Value | A | **Fail** |
| SC 4.1.3 | Status Messages | AA | Manual |

## Manual Testing Recommendations

<!-- report.js: This section should be populated by the auditing agent -->
<!-- based on Phase 4 manual check guidance, which requires reasoning -->
<!-- about the specific findings pattern. -->

## Remediation Priority

| Priority | Rule | Impact | Instances | WCAG |
|---|---|---|---|---|
| P0 | frame-title | serious | 1 | SC 4.1.2 |
| P1 | list | serious | 4 | SC 1.3.1 |
| P2 | landmark-unique | moderate | 15 | - |
| P3 | region | moderate | 8 | - |
| P3 | landmark-one-main | moderate | 2 | - |
| P3 | heading-order | moderate | 2 | - |
| P3 | page-has-heading-one | moderate | 1 | - |

## Issues Created

Issue creation was not executed by the report generator.

## Methodology

| Field | Value |
|---|---|
| Scan Date | 2026-03-26 |
| Pages Scanned | 15 |
| Viewport | 1280 x 800 |
| Browser | Headless Chromium (Puppeteer) |
| Scanner | axe-core via scan.js |
| Lighthouse | Skipped: Lighthouse disabled for this run |
| Runtime URL | https://sam-rogers.com |
| Expected URL | https://sam-rogers.com |

### Sampling Strategy

Pages were selected via template-aware sampling (discover.js). 206 total pages were classified into 12 template groups; 15 representative pages were scanned.

| Template Group | Total Pages | Scanned | Selection |
|---|---|---|---|
| `about` | 1 | 1 | top-level page — always included |
| `archive` | 1 | 1 | top-level page — always included |
| `blog` | 1 | 1 | top-level page — always included |
| `contact` | 1 | 1 | top-level page — always included |
| `now` | 1 | 1 | top-level page — always included |
| `privacy` | 1 | 1 | top-level page — always included |
| `projects` | 1 | 1 | top-level page — always included |
| `tags` | 1 | 1 | top-level page — always included |
| `blog/*` | 143 | 2 | 2 of 143 — by DOM complexity (scores: 7→2) |
| `now/*` | 52 | 2 | 2 of 52 — by DOM complexity (scores: 5→3) |
| `about/*` | 2 | 2 | all 2 — small group |
| `/` | 1 | 1 | singleton — always included |

### Shared Template Patterns

Template groups with identical violation fingerprints share the same underlying issues. Fixing the shared template resolves the issue across all pages in those groups.

- **Shared issues on `about`, `now`, `about/*`:** landmark-unique, region
- **Shared issues on `archive`, `blog`:** landmark-one-main, landmark-unique, region
- **Shared issues on `contact`, `privacy`:** heading-order, landmark-unique, region
- **Shared issues on `tags`, `/`:** landmark-unique
- **Shared issues on `blog/*`, `now/*`:** landmark-unique, list
