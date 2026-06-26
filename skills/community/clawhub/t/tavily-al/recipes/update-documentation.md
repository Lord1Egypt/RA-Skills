# Recipe: Update Documentation

## Goal
Refresh an existing document (e.g. a how-to, API reference snippet, or fact sheet) by checking current sources with Tavily, identifying outdated statements, and proposing grounded, cited corrections.

## When to use
- A document may contain stale facts (versions, dates, pricing, endpoints, names) that need verification against the live web.
- You want a diff of what changed and why, with sources.
- Do NOT use to write a document from scratch (use `build-research-brief.md`).

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `document` | Yes | The current text to review/update. |
| `TAVILY_API_KEY` | Yes | From environment. Never hardcode. |
| `authoritative_domains` | No | Official domains to prefer via `include_domains`. |
| `freshness` | No | Use `topic:"news"` + `time_range` for fast-moving facts. |

## Steps
1. **Read `TAVILY_API_KEY`** from environment; abort if missing.
2. **Extract verifiable claims** from `document` (versions, dates, numbers, URLs, names).
3. **For each claim, search** via `POST https://api.tavily.com/search`, preferring `authoritative_domains` with `include_domains`. Validate status.
4. **Extract** the official source's full text when needed to confirm exact current values.
5. **Compare** each document claim to the verified value: mark Confirmed, Outdated, or Unverifiable.
6. **Draft replacements** only for Outdated claims, grounded strictly in sources, each with a `[n]` citation.
7. **Hallucination-check** every proposed change.
8. **Return** a change list (old -> new with source) plus the updated document. Do NOT silently rewrite confirmed or unverifiable content.

## Output format
```
Documentation update review

Changes:
1. "old text" -> "new text"  (reason; [1])
2. "old text" -> "new text"  (reason; [2])

Unverifiable (left unchanged):
- "claim" (no authoritative source found)

Updated document:
<full revised text with changes applied>

Sources:
[1] Title — https://...
```

## Example
Document says "Tavily Extract supports `extract_depth: standard`." Search official docs, find the current allowed values, mark the claim Outdated, and propose the corrected value with a citation. Leave unrelated confirmed lines untouched.

## Edge cases
- **No authoritative source found:** Mark Unverifiable and leave the original text; flag for human review.
- **Source conflicts with itself or others:** Prefer the official/most recent; note the conflict.
- **Claim is opinion, not fact:** Do not "correct" it; only verify factual statements.
- **422/429:** Fix malformed queries; back off on rate limits and resume.

## Production notes
- Change only what evidence requires; preserve voice, structure, and confirmed content.
- Always show old -> new with a source so a human can review the diff.
- Date-stamp the review; documentation accuracy is time-bound.
- > Verification needed: confirm current Tavily endpoint parameters and allowed values with https://docs.tavily.com
