---
name: quality-review
description: "Evidence-first structured review with source-tiered claims. For code, notes, agent output, and research. Inspired by gstack methodology and gbrain source-tiering."
tags: [review, quality, code-review, research, methodology]
---

# Quality Review

Evidence-first structured review for code, source notes, knowledge entries, agent output, PRs, and research. Inspired by:
- **gstack:** planning discipline, self-review gates, structured output
- **gbrain:** source-tier ranking, gap analysis, confidence-aware claims
- **steipete/agent-scripts:** Cause/Provenance/Fix/Proof/Risk format

Every review ends with the standard template. Every claim is source-tiered. Every finding has a confidence level.

## Core Principles

1. **Source-tier all claims.** Not all evidence is equal. Label sources by tier:
   - **Tier 1:** Verified by direct inspection (opened the URL, ran the test, read the source)
   - **Tier 2:** Reported by a trusted source but not independently verified
   - **Tier 3:** Inference, extrapolation, or "seems likely" — flag explicitly as speculation
   - **Tier 4:** Confabulation risk — no source, plausible-looking filler

2. **Name the gap, don't fill it.** If evidence is missing, say so. Do not produce a plausible-sounding substitute (that's confabulation).

3. **One recommendation, not options.** Prefer a single best fix with rationale. Listing options without a call is indecision, not review.

4. **Self-review before delivery.** Run the checklist before handing off any review output.

## Review Output Template

```
Cause: <root cause or "not proven">
Provenance: <commit/PR/date/source tier + path or "unknown">
Best fix: <one concrete recommendation with rationale>
Refactor: <yes/no — specific shape of change>
Proof: <evidence with source tier — tests/CI/docs/URLs>
Risk: <remaining uncertainty — low/medium/high + specific unverified items>
```

### Tier Labels in Practice

```
Cause: Race condition in cache invalidation (verified: reproduced locally)
Provenance: Introduced in commit a3f2c1 (2026-05-20) — Tier 1
Best fix: Add mutex around the cache-bust path
Refactor: No — the fix is scoped, the broader cache layer is sound
Proof: Reproduced with `go test -race ./cache` — Tier 1
Risk: Low — fix is covered by existing tests + one new regression test
```

```
Cause: Not proven — the error log is real but too vague to isolate
Provenance: Error first appeared in CI run #8472 (2026-05-24) — Tier 2
Best fix: Add structured logging to the error path before attempting any fix
Refactor: No — fixing the symptom without root cause is premature
Proof: Error ID matches the pattern but cannot be deterministically reproduced — Tier 2
Risk: High — root cause still unknown, fix could mask the real issue
```

## Scope-Specific Guidance

### Source Note Review (Knowledge Curation)

- Does the note faithfully represent the source? (Check source-tier)
- Are provenance, date, and author recorded?
- Are backlinks to existing concepts present or missing?
- Is the note doing essay + hub + reference work? Recommend splitting if so.

### Code Review

- Does the change fix the stated problem?
- Edge cases, regressions, silent failures?
- Are test coverage and CI evidence clear?
- Add "Merge confidence: high/medium/low + one-sentence why."

### Agent Output Review (Self or Peer)

- Does the output follow instructions or drift?
- Are claims source-tiered or smooth guesses?
- Token efficiency — could the same content be shorter?
- `Cause` = drift/fabrication/inefficiency, `Provenance` = the instruction that should have bounded it

### Research Synthesis Review

- Are all claims backed by cited sources at Tier 1-2?
- Are gaps between sources explicitly marked as uncertainty?
- Does the synthesis conflate findings from different methodologies?
- Is the distinction between direct evidence and extrapolation clear?

## Self-Review Checklist

Before delivering any review output:

- [ ] Cause identified — or "not proven" called out honestly
- [ ] Provenance traced — with source tier
- [ ] Best fix recommended — one, not a menu
- [ ] Refactor decision made — yes/no with shape
- [ ] Proof cited — with source tier and paths/URLs
- [ ] Risk stated — specific about what remains uncertain
- [ ] No confabulated evidence — every URL opened, every claim verified
- [ ] Token budget considered — would a shorter version serve better?

## Dispatching

When dispatching a review: include the full artifact, the question you want answered, and demand the review output template in the reply. Route the review to the appropriate specialist:
- **Research/curation reviews** go to someone who understands the domain
- **Code reviews** go to someone who can run the code
- **Writing reviews** go to an editor familiar with the voice
