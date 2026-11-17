# Evidence — ui-roi-audit

**Date:** 2026-10-08  
**Version tested:** 2.0 (workflow verified as 1.1; naming and routing revised in 2.0)  
**Status:** publication-ready; behavioral and source-verification gates passed.

## Test inventory

| Test | Result |
|---|---|
| Product page, no analytics | Pass — `examples/sample-audit.md` |
| With-skill vs no-skill baseline, landing page with ROI data | With-skill wins 4, baseline wins 0, one tie |
| Trigger routing: 5 positive and 5 negative requests | 10/10 routed as intended after v2 naming and description revision |
| Task-driven interface with usability module and cost avoided | Pass |
| Checkout page, no analytics | Pass |
| Criterion-level source verification | Pass — all 54 mappings checked; six narrowed or corrected |

## Baseline comparison

### Setup

Two fresh agents received the same B2B SaaS landing-page scenario. The page had 20,000 monthly
visits, 1.2% conversion, 120 EUR lead value, and an 8,000 EUR implementation cost. The ad made a
specific 30% claim, while the page used a generic hero, competing actions, full navigation, weak
proof, and a ten-field form. One agent loaded this skill; the baseline was explicitly prohibited
from reading it. Neither used the internet.

### Results

- **With skill:** followed the eight-section report contract, attached criterion IDs and chapter
  citations to ranked findings, separated unscored form observations, named unobserved states, and
  modelled a 3–10% *relative* uplift as an assumption. Twelve-month ROI: 30–332%; payback: 2.8–9.3
  months.
- **Baseline:** produced a strong senior-level optimization plan and validation metrics, but no
  criterion IDs, source trail, explicit “not assessed” section, or separation between sourced and
  unsourced advice. It assumed a wider 10–25% relative uplift. Twelve-month ROI: 332–980%; payback:
  1.1–2.8 months.

Both calculations were arithmetically correct. The difference is epistemic discipline: the skill
did not make its uplift assumption a benchmark and chose the more conservative range.

### Five-point comparison

| # | Rubric | With skill | Baseline | Winner |
|---|---|---|---|---|
| 1 | Procedural adherence | Framed the audit, inventoried the page, scored sourced criteria, prioritized, calculated annual ROI, and reported observation limits. | Performed a good heuristic audit, but used no declared procedure and moved into replacement-copy drafting. | With skill |
| 2 | Output-contract compliance | All eight sections present; findings stayed under 15 rows and ended with the full source used. | Useful structure, but no criteria/source columns, “what passed”, “not assessed”, or source list. | With skill |
| 3 | Edge cases | Treated unobserved errors and post-submit states as not assessed; kept form-layout advice outside sourced ranking; stated model omissions. | Also rejected guaranteed uplift and protected lead quality, but treated form assumptions as recommendations without an evidence boundary. | With skill |
| 4 | Hallucinations | No invented quotations or source statistics. The 3–10% range was explicitly a scenario assumption. | No fake citations, but the 10–25% range had no grounding beyond being called conservative. | With skill |
| 5 | Justification quality | Clear page evidence and traceable reasons for each ranked finding. | Stronger experiment plan and equally useful business reasoning. | Tie |

**Score: with-skill wins 4, baseline wins 0, ties 1.**

### Verdict and resulting fix

The skill is measurably better than baseline at producing an auditable, bounded report without
weaker business reasoning. The run exposed one gap: a landing page whose conversion control is a
form loaded only landing-page criteria, leaving form defects as uncited observations. The workflow
now loads the secondary form or checkout section when that control is embedded in another page.

## Trigger routing test

This was a description-level routing test: each request was checked against the v2 discovery
description and the explicit scope boundaries in `SKILL.md`.

### Should invoke

| Request | Result | Why |
|---|---|---|
| “Zrób audyt ROI tego landing page’a i powiedz, co poprawić najpierw.” | Invoke | Explicit ROI audit and prioritization |
| “Why doesn’t this product page convert?” | Invoke | Explicit conversion diagnosis of one supported page type |
| “Rank the checkout problems by business impact.” | Invoke | Supported page type and impact ranking |
| “Czy redesign formularza się opłaci? Mam ruch, CR i koszt wdrożenia.” | Invoke | Form audit with ROI inputs |
| “Audit this support dashboard and estimate the ROI of reducing task time.” | Invoke | Task-driven interface with measurable cost impact |

### Should not invoke

| Request | Result | Route instead |
|---|---|---|
| “Napisz hero i CTA dla naszego landing page’a.” | Do not invoke | Content design / copywriting |
| “Zrób audyt SEO i research słów kluczowych.” | Do not invoke | SEO workflow |
| “Sprawdź zgodność formularza z WCAG 2.2 AA.” | Do not invoke | Accessibility audit |
| “Oceń tone of voice marki na stronie.” | Do not invoke | Brand-voice review |
| “Zagwarantuj, ile przychodu da ten redesign.” | Do not invoke | Forecast commitment is outside scope |

**Result:** 5/5 positive and 5/5 negative cases route correctly. The frontmatter description names
web pages, task-driven interfaces, conversion, usability, and ROI; exclusions remain explicit in
the body.

## Usability-module run

### Scenario

A task-driven support dashboard used by 30 agents to find the oldest unassigned high-priority
ticket, assign an owner, and reply. The queue handles 4,000 tickets a month. Current triage time is
three minutes per ticket; labor is valued at 30 EUR/hour. Search accepts only an exact ticket ID,
priority filters sit behind an unlabelled icon, assigning and closing are adjacent, the assignment
has no undo, and first-time users need a walkthrough. A proposed fix costs 5,000 EUR; the test
models 30–60 seconds saved per ticket as a scenario assumption.

### Outcome

| Factor | Score | Evidence |
|---|---|---|
| US-1 Findability | Partial | Target tickets can be found, but only after discovering the hidden filter |
| US-2 Navigation | Pass | Queue, ticket, and reply areas keep a stable structure and location |
| US-3 Search and filtering | Fail | Search requires exact ID; the relevant priority filter is hidden and unlabelled |
| US-4 Form efficiency | N/A | The tested task does not require a data-entry form |
| US-5 Error prevention and recovery | Fail | Destructive close is adjacent to assign and assignment has no undo |
| US-6 Task success | Partial | Experienced users finish; a first-time user needs help |
| US-7 Learnability | Fail | The primary filter is not self-explanatory and requires a walkthrough |
| US-8 Returning-user experience | N/A | No returning-user comparison was provided |

The module kept these findings separate from conversion content. Cost avoided was calculated from
the user's volumes, not an old case statistic: 12,000–24,000 EUR annual value, 7,000–19,000 EUR net
value, 140–380% ROI, and 2.5–5 months to payback. The result explicitly treats time saved as an
assumption to validate with before/after task timing.

**Result:** Pass. The module handles task software, N/A factors, cost avoided, ranges, and dated
evidence boundaries without forcing sales-page criteria onto the interface.

## Checkout-page run

### Scenario

A four-step retail checkout retains full site navigation, has no step indicator, requires account
creation before address entry, first reveals a 12 EUR handling fee at payment, shows no security or
guarantee reassurance near card fields, and clears correctly entered address data after a payment
validation error. No traffic, conversion, or order-value data was supplied.

### Outcome

The run detected CO-1 through CO-5 as failures and connected the same page evidence to TR-1, PR-1,
and ER-3 where applicable. It ranked removal of the surprise fee and account gate above the step
indicator, marked the ROI as qualitative, and named visits, checkout completion rate, average order
value, and implementation cost as missing inputs. It did not assign a score to mobile layout or
unseen success states.

**Result:** Pass. A second page type works end to end and missing analytics do not produce invented
numbers. The chapter attributions used in this run were checked in the source-verification pass.

## Product-page run

The original dry run remains in `examples/sample-audit.md`. It completed all six procedure steps,
kept nine findings under the table limit, marked four unobservable items as not assessed, and
handled missing analytics qualitatively. It also exposed and fixed the need for an uncited
“Observations outside the criteria” section and a viewport-based definition of exposure.

## Source-verification result

On 2026-10-08, a source-grounded NotebookLM pass checked all 54 Loveday & Niehaus criteria against
the loaded book, plus the white-paper section names, selected original-study author/year labels,
and book-publication metadata. Forty-eight criteria were retained unchanged. Six were corrected:

- CP-3 now requires recognizable, clearly framed thumbnails rather than cropping in every case.
- FM-1 now allows short related fields to share a row within a primarily vertical flow.
- FM-2 now names both top- and right-aligned label patterns.
- CO-5 now cites chapters 6, 7, and 9.
- TR-2 now requires the privacy link next to forms collecting personal data, not every possible
  collection point.
- TR-4 now also cites chapter 5.

The usability module now uses the white paper's full section names. The Bosert and Spool citations
carry their complete intermediary chains, and an unconfirmed 60–90% rework statistic was removed.
The publisher record resolves the white paper's 2004 “in press” note: the second edition of
*Cost-Justifying Usability* was published by Morgan Kaufmann in 2005, and Marcus's final chapter is
“User Interface Design's Return on Investment,” Chapter 2, pp. 17–39.

**Verdict:** all publication gates documented in this file are closed.
