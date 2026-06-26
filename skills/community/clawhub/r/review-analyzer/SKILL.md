---
name: review-analyzer
description: Extract sentiment patterns, repeated pain points, and feature requests from customer reviews to prioritize product fixes and copy improvements.
---

# Review Analyzer

This skill turns a pile of unstructured customer reviews into a ranked, evidence-backed action list. It separates *product* problems (things you fix in the factory or supply chain) from *listing-copy* problems (things you fix by setting expectations on the page), so the seller stops guessing and starts shipping changes that move conversion, return rate, and rating.

The output is a single Review Analysis report: aspect-by-aspect sentiment, frequency-and-severity-ranked pain points, an explicit feature-request list, and a prioritized backlog split into "product fixes" and "copy changes." Numbers carry the argument; quotes make it credible.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
| --- | --- | --- | --- |
| Sample size | All available reviews, or a random sample of >=150 per variant | 80-150 reviews, recent-weighted | <50 reviews, or only 5-star pulled |
| Sentiment scheme | Aspect-based (per-feature) + overall, 4-label rubric | Overall sentiment + 3-4 tagged aspects | Single star average, no text coding |
| Aspect-based vs overall | Both; aspect drives the action list | Aspect for top 5 themes only | Overall only ("people seem happy") |
| Fake / incentivized reviews | Flagged, quantified, excluded from sentiment, reported separately | Obvious bot clusters removed | Left in; treated as real signal |
| Star-vs-text mismatch | Recode to the *text* sentiment, log the mismatch rate | Note mismatches in a column | Trust the star, ignore the words |
| Theme threshold | >=3 independent mentions OR >=2% of reviews to name a theme | >=2 mentions | One vivid review becomes a "trend" |
| Severity scoring | Frequency x impact (return/safety/refund risk), 1-5 | Frequency rank only | Loudest complaint wins |
| Copy-vs-product routing | Every pain point tagged PRODUCT, COPY, or BOTH with rationale | Routed for top issues | "We'll fix it somehow" |
| Time / version handling | Segmented by month and SKU/variant; pre/post change compared | Split old vs new at a known change date | All-time blob, no trend |
| Quote handling | Verbatim, de-identified, linked to review ID | Paraphrased with ID | No quotes, just adjectives |

## Solves

- **"Our rating dropped and we don't know why."** Pinpoints which aspect (e.g., zipper, battery, sizing) is dragging the average and when it started.
- **High return rate with vague reasons.** Maps returns-language in reviews to specific, fixable causes (wrong size chart, misleading photo, fragile part).
- **Roadmap by gut feel.** Replaces "the CEO read one angry review" with a frequency-and-severity-ranked backlog.
- **Listing copy that oversells.** Surfaces the gap between what the page promises and what the text says buyers actually got, so copy can be corrected before it generates more bad reviews.
- **Lost feature requests.** Collects the "I wish it had..." comments that are scattered across hundreds of reviews and almost never reach the product team.
- **Competitor comparison blind spots.** Extracts the "I switched from Brand X because..." statements that reveal your real differentiators and weaknesses.
- **No way to prove a fix worked.** Establishes a baseline so a later re-run shows whether sentiment on a fixed aspect actually improved.

## Workflow

1. **Gather and clean the corpus.** Pull every available review for the product (and close variants) with star rating, date, variant/SKU, verified-purchase flag, and review ID. Normalize encoding, strip duplicate/templated spam, and flag incentivized or suspicious reviews (see the sentiment guide) rather than deleting them silently. Record the date range and total counts before and after cleaning so the report is reproducible.

2. **Segment before you read.** Split the corpus by star rating (1-2 / 3 / 4-5), by variant/color/size, and by time window (typically by month, or pre/post a known product change). Segmentation is where most insights hide: an aspect can look fine overall while one variant is on fire. Decide your time pivot now (e.g., the date a new supplier shipped).

3. **Code sentiment and aspects.** Apply the 4-label rubric (positive / neutral / negative / mixed) to each review's *text*, and tag the aspects mentioned (quality, sizing, shipping, accuracy, value, usability, service, missing-features). Always code from the words, not the stars; log every star-vs-text mismatch. For large corpora, draft an automated pass, then hand-verify a 10-15% random sample for inter-rater consistency.

4. **Cluster pain points and requests.** Group negative and mixed mentions into themes using the pain-point taxonomy; merge synonyms ("runs small," "too tight," "size up" -> Sizing/Fit). Separately collect explicit feature requests ("wish it had a longer cord"). Only promote a cluster to a named theme once it clears the threshold (>=3 independent mentions or >=2% of reviews).

5. **Quantify frequency and severity.** For each theme, count mentions, compute its share of reviews, note the trend across time windows, and score severity = frequency x impact, where impact reflects return/refund/safety risk and rating drag. A 6%-frequency safety complaint outranks a 12%-frequency cosmetic nitpick.

6. **Route to product vs listing copy.** Tag every theme PRODUCT, COPY, or BOTH. Ask: "Would the buyer still be unhappy if the page had set the right expectation?" If yes, it's PRODUCT. If the item is fine but the page oversold or under-informed, it's COPY. Many sizing and accuracy issues are BOTH — fix the chart now (copy) while you tweak the pattern next run (product).

7. **Output the report and track.** Fill the output template: overview, aspect sentiment table, ranked pain points, feature requests, and a prioritized action list split into product fixes and copy edits with owners and expected impact. Set a re-run date (e.g., 60-90 days post-change) and record the baseline so improvement is measurable.

## Example 1

**Product:** "TrailLite 30L Packable Hiking Backpack" — $48, one SKU, 3 colors.
**Corpus:** 214 reviews pulled, date range 2025-09-01 to 2026-05-31. After removing 9 templated/incentivized and 2 duplicates: **203 analyzed.** Avg rating 4.1. Distribution: 5* 49%, 4* 22%, 3* 9%, 2* 8%, 1* 12%. Star-vs-text mismatch rate: 7% (mostly 3-4* reviews whose text was clearly negative — recoded).

**Aspect sentiment (of reviews mentioning the aspect):**

| Aspect | Positive % | Negative % | # Mentions | Trend |
| --- | --- | --- | --- | --- |
| Weight / packability | 91% | 6% | 142 | Stable |
| Capacity / fit of gear | 78% | 18% | 96 | Stable |
| Zippers / hardware | 41% | 55% | 88 | Worsening (Jan->May) |
| Shoulder-strap comfort | 63% | 33% | 71 | Stable |
| Water resistance | 30% | 64% | 47 | Worsening |
| Value for price | 80% | 14% | 61 | Stable |

**Top pain points:**

| Issue | Count | Severity (1-5) | Route |
| --- | --- | --- | --- |
| Zipper splits / slider fails | 48 (24%) | 5 | PRODUCT |
| "Water resistant" leaks in rain | 30 (15%) | 4 | BOTH |
| Straps dig in when loaded >8kg | 22 (11%) | 3 | BOTH |
| Smaller than expected vs photos | 14 (7%) | 2 | COPY |

**Feature requests:** sternum strap (11), internal laptop sleeve (7), hip belt (6).

**Resulting actions —**
*Product fixes:* (1) Replace the #5 nylon zipper/slider with a #8 coil + metal slider; the worsening Jan->May trend tracks a documented supplier change — escalate as priority 1. (2) Add foam padding to the strap pattern for the next run.
*Copy changes (ship this week):* (1) Change "waterproof"/"water resistant" to "water-repellent for light drizzle; not for sustained rain — rain cover sold separately" and add a rain-cover cross-sell. (2) Add a packed-vs-expanded dimension photo with a 1L bottle for scale to kill the "smaller than expected" returns. (3) Update bullet to note it carries best up to ~8kg.

## Example 2

**Product:** "GlowDesk LED Monitor Light Bar — USB-C, Auto-Dim" — $39, 2 variants (Standard, Pro w/ remote).
**Corpus:** 168 reviews, 2025-11-01 to 2026-06-10. After cleaning 6 fake (5-star clusters posted same day, generic text): **162 analyzed.** Avg 3.8. Distribution: 5* 41%, 4* 19%, 3* 11%, 2* 11%, 1* 18%.

**Aspect sentiment:**

| Aspect | Positive % | Negative % | # Mentions | Trend |
| --- | --- | --- | --- | --- |
| Light quality / no glare | 86% | 9% | 119 | Stable |
| Mounting clip fit | 38% | 58% | 77 | Stable |
| Auto-dim sensor behavior | 44% | 49% | 64 | Worsening (Pro only) |
| USB-C cable length | 35% | 61% | 52 | Stable |
| Remote (Pro) | 52% | 41% | 33 | Stable |
| Build / materials | 71% | 22% | 58 | Stable |

**Top pain points:**

| Issue | Count | Severity | Route |
| --- | --- | --- | --- |
| Clip won't grip monitors <8mm or curved | 41 (25%) | 4 | BOTH |
| Cable too short for tower-on-floor setups | 31 (19%) | 3 | BOTH |
| Auto-dim flickers / over-dims (Pro firmware) | 28 (17% of Pro) | 4 | PRODUCT |
| Remote pairing drops | 13 (8% of Pro) | 3 | PRODUCT |

**Feature requests:** longer/detachable cable option (24), adjustable color temperature (15), clip shims for thin monitors (9).

**Resulting actions —**
*Product fixes:* (1) Ship Auto-dim firmware fix and remote-pairing fix — both isolated to the Pro variant and the auto-dim trend is worsening; priority 1. (2) Redesign clip with a wider gripping range / include a foam shim insert (the most-requested feature would also defuse the #1 complaint).
*Copy changes (ship this week):* (1) Add a compatibility line: "Fits flat monitors 8-32mm thick; not designed for curved or ultra-thin (<8mm) panels" with a measure-your-bezel diagram — this is the single biggest return driver. (2) State exact cable length (1.2m) in a bullet and add a "need more reach?" extension-cable cross-sell. (3) Add a short clip-fit photo set. These three copy edits alone target ~44% of all negative reviews without touching the hardware.

## Common Mistakes

1. **Reading only 1-star reviews.** You'll over-index on rare disasters and miss the broad mild dissatisfaction in 3-4* text. *Fix:* sample across all ratings; the 3* reviews are the most diagnostic.
2. **Trusting the star, ignoring the words.** A 4-star review that says "great but the strap broke in a month" is a negative durability signal. *Fix:* code sentiment from text and track the mismatch rate.
3. **Promoting an anecdote to a trend.** One eloquent rant is not a pattern. *Fix:* enforce the >=3-mention / >=2% threshold before naming a theme.
4. **Counting mentions but ignoring severity.** Twelve "wish it came in blue" comments are not more urgent than five "it overheated." *Fix:* score severity = frequency x impact (return/safety/refund risk).
5. **Leaving fake/incentivized reviews in the sentiment math.** They inflate positives and hide real problems. *Fix:* flag, quantify, exclude from sentiment, report the rate separately.
6. **Analyzing all variants as one blob.** A defect isolated to the Pro firmware or the black colorway gets diluted to "minor." *Fix:* segment by variant/SKU and time before computing percentages.
7. **No time trend.** An all-time average hides a defect that started last month after a supplier change. *Fix:* segment by month; flag worsening/improving aspects.
8. **Routing everything to "product."** Many complaints are expectation gaps that a copy edit fixes today. *Fix:* tag every theme PRODUCT / COPY / BOTH with a written rationale.
9. **Mishandling negation and sarcasm.** "Not bad at all" is positive; "Oh great, broke day one" is negative. *Fix:* follow the negation/sarcasm rules in the sentiment guide; spot-check the automated pass.
10. **Percentages with no denominator.** "55% negative on zippers" is meaningless without knowing 55% of *how many mentions*. *Fix:* always report the # of mentions alongside the %.
11. **No baseline, no follow-up.** Without a recorded baseline you can never prove the fix worked. *Fix:* store the report and set a 60-90 day re-run.
12. **Quoting without de-identifying or sourcing.** *Fix:* use verbatim, de-identified quotes tied to a review ID for traceability.

## Resources

- [`references/output-template.md`](references/output-template.md) — fill-in template for the finished Review Analysis report.
- [`references/sentiment-coding-guide.md`](references/sentiment-coding-guide.md) — the labeling rubric, edge-case handling, fake-review red flags, and consistency tips.
- [`references/pain-point-taxonomy.md`](references/pain-point-taxonomy.md) — standard pain-point categories with phrasings, product-vs-copy routing, and the proactive copy fix for each.
- [`assets/quality-checklist.md`](assets/quality-checklist.md) — pre-publish QA checklist covering data, sampling, coding, clustering, quantification, routing, and reporting.
