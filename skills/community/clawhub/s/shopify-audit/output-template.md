# Output Template — Shopify Conversion Audit Report

## 1. Executive Snapshot

```
Store: [URL, theme if identifiable]
Primary audit target: [PDP/collection URL]
Traffic profile: [device split, top source]
Baseline: [conversion %, ATC %, checkout completion % — or "not provided"]
Audit date: [date]
Top 3 wins: [one line each — the findings to do this week]
```

## 2. Scorecard

| Funnel stage | Score (1–5) | Headline issue |
|---|---|---|
| Homepage first impression | | |
| Collection browsability | | |
| Product page persuasion | | |
| Cart & checkout | | |
| Performance & mobile | | |

## 3. Prioritized Findings (max 15)

Each finding in this exact format:

```
#N — [Page] — Impact: High/Med/Low — Effort: S/M/L
Issue:    [what blocks the buyer, one sentence]
Evidence: [what was observed + why it matters for THIS store's traffic profile]
Fix:      [executable instruction: exact rewrite, theme-editor path
           (e.g., Theme > Customize > Product > add Rating block), or app/setting change]
```

Sorting rule: estimated revenue impact (page traffic × severity) descending, effort as tiebreaker. High-impact/small-effort items always rank above high-impact/large-effort.

## 4. Copy Rewrites Appendix

For every copy finding, provide before → after:

```
Location: [page + element]
Before:   [current text]
After:    [rewritten text]
Why:      [benefit-led / objection handled / length cut]
```

## 5. Performance Summary

```
LCP (PDP, mobile): [x.x s]  → target <2.5s
Heaviest assets: [top 3 with sizes]
App scripts: [count installed / count recommended for removal or defer]
Image format status: [WebP/AVIF coverage]
```

## 6. Mobile Pass Notes

Thumb-reach of ATC, sticky ATC presence, tap-target spacing, type legibility, content covered by sticky elements — pass/fail each with location.

## 7. Re-audit Schedule

State the trigger for the next audit (quarterly, pre-BFCM, post-theme-change) and the 3 metrics to compare against baseline.

## Quality gates

- Every finding names the blocked buyer behavior, not an aesthetic preference
- Every fix is executable as written (rewrite text provided, editor path named)
- Findings sorted by impact × effort; list capped at 15
- Mobile pass present for any store >50% mobile traffic
- No fake-urgency recommendations; honesty flags included where found
