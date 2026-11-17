# Report Artifact

Create a standalone HTML report from the final qualified prospect data. Use the bundled generator instead of writing report markup manually.

## Generate

```bash
python3 scripts/generate_report.py analysis.json outputs/signal-scout-report.html
```

Return a clickable absolute file link in the final response. Keep the JSON in a work or temporary directory unless the user asks for raw data.

If `analysis.json` lives alongside prior snapshots saved per the SKILL.md storage convention (`outputs/<slug>/analysis-<date>.json`), the generator auto-detects every sibling `analysis-*.json` (excluding the input itself) and a sibling `outcomes.jsonl`, then badges each prospect **New**, **Seen Nx**, or **Resurfacing** — see "Novelty fields" below. Override with `--history a.json b.json ...` (explicit list instead of auto-detection), `--no-history` (skip novelty entirely), or `--outcomes path.jsonl` (explicit outcomes file).

## JSON schema

This file is the schema authority — SKILL.md holds only a compact summary. Draft against this, then run `scripts/finalize.py --validate-only analysis.json` to machine-check it instead of re-reading these rules.

### Top-level shape

```json
{
  "title": "string — short product name",
  "product": "string — one-line product description",
  "product_url": "string — product URL",
  "target_customer": "string — primary ICP description",
  "adjacent_icp": "string — secondary ICP (optional)",
  "search_scope": "string — e.g. 'Public English-language sources, last 12 months'",
  "generated_at": "string — ISO date YYYY-MM-DD",
  "methodology": "string — 1-2 sentence summary of research approach",
  "search_queries_used": ["string — each query issued during research"],
  "sources_consulted": ["string — each source URL or platform visited"],
  "verdict": "string — whether the startup has reachable early-customer signals",
  "individuals": ["see Individual schema"],
  "segments": ["see Segment schema"],
  "companies": ["see Company schema"],
  "patterns": ["see Pattern schema"],
  "outreach_plan": "see Outreach plan schema",
  "competitive_context": "see Competitive context schema (optional)",
  "limits": ["string — missing evidence, assumptions, and classification calls"],
  "people": "boolean (optional): false turns on no-people mode for finalize.py and generate_report.py, same as --no-people"
}
```

With `"people": false` (or `finalize.py --no-people`), the published output carries no Individuals, and person names, handles, personal emails, and profile URLs that match the filter's patterns are redacted from every field. It is a pattern filter, not a guarantee. finalize.py writes it to a `public/` folder next to the input and leaves the input untouched. See COMPLIANCE.md for exactly what the filter catches and what it does not.

At least one of `individuals`, `segments`, `companies` must be non-empty. Omit an array entirely rather than including it empty.

### Individual schema

```json
{
  "name": "string — real name or stable public handle",
  "stage": "string — High intent | Problem aware | Trigger present | Potential fit",
  "score": "number 0-100",
  "pain_signal": "string — the specific public pain or demand signal",
  "evidence": "string — what was observed and where",
  "why_fit": "string — why the product solves their stated problem",
  "why_now": "string — what timing trigger makes this relevant today",
  "source_title": "string — title of the source page or post",
  "source_url": "string — valid URL to the public source",
  "source_type": "string — Forum | Social post | Review | GitHub issue | Company page | Changelog | Job post | Directory | Other",
  "signal_date": "string — publication date if visible, else 'Date unavailable'",
  "suggested_channel": "string — recommended outreach channel, or 'No public reply/DM channel exists' if none",
  "opener": "string — suggested first message under 90 words, or omit if no channel exists",
  "follow_up_sequence": ["string — 2-3 follow-up messages for the outreach companion skill"],
  "caution": "string — risk or caveat before outreach",
  "competitor_mentioned": "string — competitor they currently use or mentioned (optional)",
  "dimensions": {
    "pain_strength": "number 0-5",
    "product_fit": "number 0-5",
    "timing": "number 0-5",
    "reachability": "number 0-5",
    "evidence_quality": "number 0-5"
  }
}
```

If `suggested_channel` is "No public reply/DM channel exists," omit `opener` and `follow_up_sequence` rather than writing "N/A" — the report generator treats a missing field as not applicable, not a filled-but-empty one.

### Segment schema

```json
{
  "name": "string — short segment name, e.g. '[Competitor] comparison-shoppers'",
  "stage": "string — High intent | Problem aware | Trigger present | Potential fit",
  "score": "number 0-100",
  "pain_signal": "string — the repeated pain or demand pattern",
  "evidence": "string — what was observed and where (aggregate, not one post)",
  "why_fit": "string — why the product solves this pattern's job-to-be-done",
  "why_now": "string — what makes this pattern current",
  "source_title": "string",
  "source_url": "string",
  "source_type": "string",
  "signal_date": "string",
  "content_angle": "string — the searchable or shareable angle to take (see research-framework.md)",
  "target_keywords": ["string — search terms this segment actually uses"],
  "suggested_channels": ["string — e.g. SEO/blog, ASO, Reddit reply-when-relevant, YouTube comparison"],
  "proof_points": ["string — evidence-backed claims to use in the content"],
  "caution": "string",
  "competitor_mentioned": "string (optional)",
  "dimensions": {
    "pain_strength": "number 0-5",
    "product_fit": "number 0-5",
    "timing": "number 0-5",
    "evidence_quality": "number 0-5"
  }
}
```

### Company schema

```json
{
  "name": "string — organization name",
  "role": "string — Potential customer account | Integration/distribution partner | Expansion partner",
  "stage": "string — High intent | Problem aware | Trigger present | Potential fit",
  "score": "number 0-100",
  "pain_signal": "string — the product gap or business trigger",
  "evidence": "string — what was observed and where",
  "why_fit": "string — the combined value proposition: what this unlocks for both sides",
  "why_now": "string — the trigger event or timing signal",
  "source_title": "string",
  "source_url": "string",
  "source_type": "string",
  "signal_date": "string",
  "execution_path": "string — Self-serve program | Warm BD | Cold BD",
  "contact_path": "string — the public channel (e.g. 'self-serve developer platform signup,' 'corporate partnerships page') — never a scraped personal contact",
  "bd_angle": "string — suggested opening pitch, under 90 words",
  "what_to_propose": "string — the concrete first ask",
  "caution": "string",
  "domain": "string (optional): bare company domain such as 'acme.com', no scheme or path. Exported as the CSV `domain` column, which Clay and CRMs match company records on",
  "dimensions": {
    "strategic_fit": "number 0-5",
    "timing": "number 0-5",
    "execution_ease": "number 0-5",
    "evidence_quality": "number 0-5"
  }
}
```

### Pattern schema

```json
{
  "title": "string — short pattern name",
  "count": "number — how many prospects (any type) show this pattern",
  "insight": "string — what this means for positioning or outreach"
}
```

### Outreach plan schema

```json
{
  "angle": "string — the core outreach strategy",
  "first_step": "string — what to do first",
  "follow_up": "string — what to do after initial contact",
  "success": "string — what success looks like in 7 days",
  "channels_to_prioritize": ["string — ranked list of outreach channels"],
  "personalization_notes": "string — how to personalize beyond templates"
}
```

### Competitive context schema

```json
{
  "top_competitors": ["string — 3-5 competitors the prospects likely use"],
  "switching_barriers": "string — what makes switching hard",
  "differentiation_angle": "string — the clearest reason to choose this product instead",
  "battlecard": ["see Battlecard entry schema (optional)"]
}
```

### Battlecard entry schema (optional)

Each entry is a **new factual claim about a competitor and is verified exactly like a prospect** — `verify_sources.py` fetches `source_url` and checks `evidence` containment. A disqualified entry (Not on page / Broken source) is dropped from the report and handoff but does not fail the run. Entries are also cross-examined against the run's own prospects: `corroboration_count` counts prospects whose `competitor_mentioned` matches, and a zero-corroboration entry is badged **Single-source** on the report.

```json
{
  "competitor": "string — competitor name",
  "claim": "string — where their users complain, in one sentence",
  "evidence": "string — text actually on the source page, quoted not summarized",
  "source_title": "string",
  "source_url": "string — valid URL; required, this claim gets verified",
  "signal_date": "string (optional)",
  "switching_barrier": "string — what keeps their users locked in (optional)",
  "counter_angle": "string — the evidence-backed reason this product wins that complaint"
}
```

`verification_tier` / `verification_note` / `verified_at` / `corroboration_count` / `corroboration_note` are set by `verify_sources.py`, never authored by hand.

### Executive summary schema (optional)

The client-facing "what we did, what we found, what to do Monday" block, rendered directly under the hero. **Synthesis only:** every statement must trace to a verified prospect's fields — this section introduces no new external claims and therefore carries no verification badge of its own. Omit it for a founder's own quick run; include it when the report is a deliverable someone else will read.

```json
{
  "overview": "string — 2-3 sentences: scope, approach, and the verdict in plain language",
  "key_findings": ["string — the 3-5 findings that change what the reader does next"],
  "next_steps": ["string — concrete Monday-morning actions, most actionable first"]
}
```

### Company account tiers (optional)

Any company may carry `tier` (1, 2, or 3) and `tier_rationale` (required when `tier` is present). When at least one company is tiered, the report renders companies grouped as **Tier 1 — pursue now** / **Tier 2 — nurture** / **Tier 3 — monitor** (untiered companies fall into their own trailing group); with no tiers the flat section renders as before. Tier is an execution-priority judgment (see research-framework.md "Account tiering"), not a restatement of the score — a high-scoring company with a slow path can be Tier 2.

### Required top-level fields

| Field | Type | Notes |
|---|---|---|
| `title` | string | Short product name |
| `product` | string | One-line product description |
| `product_url` | string | Valid HTTP/HTTPS URL |
| `target_customer` | string | Primary ICP description |
| `search_scope` | string | Research scope summary |
| `generated_at` | string | ISO date YYYY-MM-DD |
| `verdict` | string | Whether the startup has reachable early-customer signals |
| `patterns` | array | 0-10 repeated signal patterns |
| `outreach_plan` | object | Seven-day outreach strategy |
| `limits` | array | 1+ strings disclosing missing evidence |

At least one of `individuals`, `segments`, `companies` (each an array, 0-20 items) must be present and non-empty. Omit an array entirely if empty — don't include `"individuals": []`.

### Optional top-level fields

| Field | Type | Notes |
|---|---|---|
| `adjacent_icp` | string | Secondary ICP description |
| `methodology` | string | 1-2 sentence research approach summary |
| `search_queries_used` | array of strings | Every query issued during research |
| `sources_consulted` | array of strings | Every source URL or platform visited |
| `competitive_context` | object | Competitor landscape |
| `growth_playbook` | object | Underserved-niche / creator-UGC growth angle — see schema below. Category-agnostic; omit entirely if you have nothing evidence-adjacent to say, don't fill it with generic creator-economy filler just to populate the section. |

### Growth playbook schema (optional)

Use this only when the research surfaced a real "high-usage, low public-visibility" pattern worth calling out — not as a default section for every report. It renders as a section titled "The invisible-user play," omitted entirely if `niches`, `agents`, and `creator_program` are all empty.

```json
{
  "thesis": "string — 1-2 sentences on why an underserved/silent-usage niche is a growth opportunity for this specific product",
  "niches": [
    {
      "name": "string — the niche or user group",
      "why_silent": "string — why this niche uses the product but doesn't post about it publicly",
      "signal": "string — evidence from this run's research supporting the niche, not a generic claim"
    }
  ],
  "creator_program": {
    "b2c_cpm": "string — short figure, e.g. '~$5', not a full sentence",
    "b2b_cpm": "string — short figure, e.g. '~$15-25', not a full sentence",
    "angle": "string — the concrete creator-outreach approach for this product"
  },
  "agents": [
    { "name": "string — short agent name", "job": "string — one-line description of what it automates" }
  ]
}
```

Keep `b2c_cpm`/`b2b_cpm` to bare figures — the report renders them as large bold numbers, and a full parenthetical sentence there breaks the layout. Put explanation in `angle` instead. Flag in `limits` that any CPM/economics figures are planning estimates, not sourced data, unless they were actually verified.

### Prospect validation rules

Common to all three types:
- `name` must be non-empty.
- `source_url` must be a valid HTTP/HTTPS URL.
- `stage` must be one of: "High intent", "Problem aware", "Trigger present", "Potential fit".
- `score` must be 0-100, calculated from that type's dimension set.
- Every prospect with score >= 50 must have a source URL that resolves.

Per type:
- **Individual**: `dimensions` must include all 5 keys (`pain_strength`, `product_fit`, `timing`, `reachability`, `evidence_quality`), each 0-5. If `opener` is present, `suggested_channel` must not be "No public reply/DM channel exists."
- **Segment**: `dimensions` must include the 4 keys (`pain_strength`, `product_fit`, `timing`, `evidence_quality`), each 0-5. `content_angle` is required.
- **Company**: `dimensions` must include the 4 keys (`strategic_fit`, `timing`, `execution_ease`, `evidence_quality`), each 0-5. `execution_path` and `contact_path` are required.

These rules are also enforced in code by `scripts/signal_scout_core.py` (`validate_prospect`, `compute_score`) — import it rather than re-deriving the weights/rules if you're scripting against report JSON directly.

### Verification fields (optional, set by `verify_sources.py`)

| Field | Type | Notes |
|---|---|---|
| `verification_tier` | string | One of `verified`, `snippet_only`, `low_match`, `unsupported`, `unverified`, `broken` — set by `scripts/verify_sources.py --annotate-out`, never authored by hand. |
| `verification_note` | string | Human-readable detail (e.g. the containment scores, or why a source was unreachable). Empty string when `verification_tier` is `verified`. |
| `verified_at` | string | ISO date (`YYYY-MM-DD`) the check ran, stamped unconditionally regardless of tier — a broken source was still checked at a point in time. `generate_report.py` renders it as a muted "· Nd ago" suffix on the verification badge once the report has been open a day or more, computed client-side against the viewer's own clock so a reopened static HTML file always shows its true age instead of looking permanently fresh. |
| `opener_grounding_note` | string | Individual-only. Set when the prospect's `opener` references specifics not present in its own `evidence` — a softer, separate check from `verification_tier` (that compares evidence to the live page; this compares the opener to the evidence text, and tolerates paraphrase by design). Renders as an inline warning below the opener on the card. Does not fail `verify_sources.py`'s exit code or drop the prospect — it's a caution to tighten the message before sending, not a disqualification. |

When present, `generate_report.py` renders a verification badge on the card (Verified / Snippet-only / Paraphrased / Not on page / Broken source) and includes a `verification` column in the CSV export. Absent entirely if `verify_sources.py` hasn't been run against the report yet — the report renders normally either way. `verified_at` and `opener_grounding_note` are HTML-only additions — neither appears in the CSV export.

**`evidence` must be text that is actually on the page.** The verifier checks containment: it fetches `source_url` and looks for the evidence's word sequences and distinctive terms in the live page. Quote the source; don't summarise it. A summary written in your own words scores as `low_match` ("Paraphrased") at best, and a claim assembled from a search snippet without opening the page scores `unsupported` ("Not on page") and fails the run. This is deliberate — `unsupported` is the fabrication signal, and it is the only check in the pipeline that a self-graded `evidence_quality` rating cannot fake, because the model rating the evidence is the model that wrote it.

### Novelty fields (optional, set by `generate_report.py`)

| Field | Type | Notes |
|---|---|---|
| `_novelty` | object | Added in-memory when history snapshots are available (auto-detected sibling `analysis-*.json` files, or passed via `--history`) — never authored by hand and never written back to `analysis.json`. Shape: `{"is_new": bool, "times_seen": int, "first_seen": "YYYY-MM-DD", "prior_outcome": "<outcome> on <date>"}`; the last three keys are present only when applicable. |

Renders as a badge next to the verification badge, reusing `diff_reports.py`'s own cumulative history (`accumulate_history`) and outcome index (`OutcomeIndex`) so both compute "have we seen this before" the same way:

- **New** — never seen in any prior snapshot saved for this product.
- **Seen Nx** — seen in N total snapshots including this one; hover shows the first-seen date.
- **Resurfacing** — recurring *and* already has a logged outcome in `outcomes.jsonl` (via `log_outcome.py`) — takes priority over the plain Seen-Nx badge, since resurfacing an already-decided prospect (`no_reply`, `not_pursued`, etc.) without a new angle just repeats a decision already made; hover shows the outcome and date.

Absent entirely if no history snapshots were found and none were passed explicitly, or `--no-history` was used — the report renders normally either way.

### Completeness scoring

The report generator calculates a completeness score (0-100) based on:

| Criterion | Points |
|---|---|
| Product brief complete | 10 |
| Methodology documented | 5 |
| Search queries logged | 5 |
| Sources consulted logged | 5 |
| Verdict present | 5 |
| 5+ prospects (any type) with scores | 15 |
| 3+ patterns with counts | 10 |
| Outreach plan complete | 10 |
| Competitive context present | 10 |
| Limits disclosed | 5 |
| Research audit present | 5 |
| All source URLs valid | 10 |

The completeness score appears in the report header as a badge.

## Report sections

The HTML report renders these sections in order:

1. **Hero** — title, date, verdict, completeness badge
2. **Stats bar** — product, target customer, high-intent count, average score, completeness
3. **Best in category** — the top-scoring Individual, Segment, and Company shown as separate call-outs (only the types present in the data get a call-out — never a single cross-type "best overall")
4. **Individuals** — "People to message": each with signal, fit, channel, opener, evidence, and 5-dimension breakdown
5. **Segments** — "Markets to target": each with pain pattern, content angle, keywords, channels, evidence, and 4-dimension breakdown
6. **Companies** — "Partners to pitch": each with gap/trigger, execution path, contact path, BD angle, evidence, and 4-dimension breakdown
7. **Repeated patterns** — signals appearing across multiple prospects of any type
8. **Growth playbook** — "The invisible-user play": underserved niches, creator-UGC economics, automation agents (if `growth_playbook` provided)
9. **Competitive context** — top competitors, switching barriers, differentiation (if provided)
10. **Seven-day outreach plan** — manual validation sequence
11. **Research audit** — queries issued, sources consulted, methodology (if provided)
12. **Limits** — missing evidence and assumptions

Sections 4-6 are omitted entirely when their array is empty or absent — the report never shows an empty "Companies" section with a placeholder card. Section 8 is omitted entirely when `growth_playbook` is absent or all of its sub-fields are empty.

The toolbar also includes an **Export CSV** button — flattens every prospect (individuals, segments, companies) into one CSV with columns `type, name, domain, stage, score, verification, pain_signal, why_fit, why_now, source_title, source_url, source_type, signal_date, next_action, caution` for pasting into a spreadsheet or CRM. `verification` is blank unless `verify_sources.py --annotate-out` was run first.

## Error handling

Common JSON issues and fixes:

| Error | Fix |
|---|---|
| `Missing prospects` | At least one of `individuals`/`segments`/`companies` must be non-empty |
| `Invalid source_url` | Ensure URL starts with http:// or https:// |
| `Score out of range` | Score must be 0-100; dimensions 0-5 |
| `Invalid stage` | Use exact strings: "High intent", "Problem aware", etc. |
| `Wrong dimension set for type` | Individual needs 5 keys incl. `reachability`; Segment/Company need 4 keys matching their own schema |
| `Empty patterns` | Provide at least one pattern or omit the field |

If the script fails twice, output the JSON directly and note the issue.
