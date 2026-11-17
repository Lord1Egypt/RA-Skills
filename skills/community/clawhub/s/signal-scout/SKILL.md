---
name: signal-scout
description: Turn a startup URL or product description into an evidence-backed, source-verified shortlist of first customers (people to message), market segments (audiences to target with content), and companies (partners to pitch) — using public signals only. Use when the user wants to find early customers, validate demand, research prospects, or plan first outreach for a product.
license: MIT
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/signal-scout
    requires:
      bins: [python3, curl]
---

# Signal Scout

Turn a startup URL or product description into a short, evidence-backed map of who has a reason to care right now. Use public signals, preserve privacy, and keep three genuinely different kinds of leads separate instead of forcing them into one ranked list.

Read [references/research-framework.md](references/research-framework.md) before researching or scoring. Read [references/report-artifact.md](references/report-artifact.md) before creating the final report.

After delivering a report, check [references/roadmap.md](references/roadmap.md) for standing follow-up ideas (feedback loop, watch mode, vertical query packs, etc.) and surface any that fit this run as an optional next step — propose them, don't build them without explicit user approval.

## Research Tools

This skill is host-agnostic — it runs anywhere an agent has these capabilities (Claude Code, Claude Cowork, OpenCode, Codex, or any agentskills-compatible host). Map each capability to whatever your environment names it:

- **Web search** — find public pain, demand, and timing signals across forums, social posts, reviews, GitHub issues, and company pages.
- **Web fetch** — open specific URLs found during research to read full pages, extract evidence, and verify claims.
- **Browser automation** (if available) — for content a plain fetch cannot render (use sparingly; respect paywalls and login walls).
- **GitHub search** (if available) — public repositories, issues, feature requests, and project activity.
- **Shell** — to run the Python scripts in `scripts/` (stdlib only, Python 3.10+).

If your host supports subagents/parallel tasks, use them to cover multiple query buckets simultaneously; otherwise run the buckets sequentially — the workflow does not depend on parallelism.

## Three prospect types — classify before you score

Every lead you find is exactly one of these. Don't blend them into one undifferentiated list — that's what made earlier reports feel generic (segments and companies forced through an "opener" field that didn't apply, scored on dimensions like "reachability" that don't mean the same thing for a person vs. an audience vs. an org).

| Type | What it is | Classification test | Next action |
|---|---|---|---|
| **Individual** | One specific, addressable person | Is there a real name or stable handle you could plausibly reply to, DM, or comment at? | Outreach opener + follow-up sequence |
| **Segment** | An audience, community, or repeated pattern — not one person | Does the evidence describe a pattern across many people, or search/demand intent with no single addressable person? | Content/GTM angle (SEO, ASO, community presence) |
| **Company** | A named organization evaluated as an account or partner | Is the value in the org's assets (customer base, platform, program) rather than one person's reply? | BD/partnership pitch |

**Edge case:** a solo maintainer or one-person company who posts publicly and is personally reachable is an **Individual** — a person is always the more actionable unit when one is available. Only classify as **Company** when what matters is the organization itself (its developer platform, its partnerships program, its customer base) and there's no single person's public post to reply to.

Log every classification call that wasn't obvious in the `limits` array.

## Structured Output

The skill produces a JSON artifact (`analysis.json`) that feeds the report generator. The full field-by-field schema lives in [references/report-artifact.md](references/report-artifact.md) — read it before drafting the JSON. The shape in brief:

- **Top level:** `title`, `product`, `product_url`, `target_customer`, `search_scope`, `generated_at`, `methodology`, `search_queries_used`, `sources_consulted`, `verdict`, `outreach_plan`, `limits`, plus optional `adjacent_icp`, `competitive_context`, `patterns`. At least one of `individuals` / `segments` / `companies` must be non-empty; omit an array entirely rather than including it empty.
- **Every prospect (all three types):** `name`, `stage` (High intent | Problem aware | Trigger present | Potential fit), `score` 0-100 computed from `dimensions` (0-5 each), `pain_signal`, `evidence` (text actually on the source page — quoted, not summarized), `why_fit`, `why_now`, `source_title`, `source_url`, `source_type`, `signal_date`, `caution`.
- **Individual adds:** `suggested_channel`, `opener` (<90 words, omit — never "N/A" — if no public channel exists), `follow_up_sequence`; dimensions are pain_strength, product_fit, timing, reachability, evidence_quality.
- **Segment adds:** `content_angle`, `target_keywords`, `suggested_channels`, `proof_points`; dimensions drop reachability (an audience isn't reachable).
- **Company adds:** `role`, `execution_path` (Self-serve program | Warm BD | Cold BD), `contact_path` (public channel only), `bd_angle` (<90 words), `what_to_propose`; dimensions are strategic_fit, timing, execution_ease, evidence_quality.

**Client-deliverable sections (optional — include when the report is a deliverable someone else will execute from, e.g. an agency's client or a team; skip for a founder's own quick run):**

- `executive_summary` — overview + key findings + Monday-morning next steps. **Synthesis only**: every statement must trace to a verified prospect's fields; it may introduce no new external claims.
- Company `tier` (1/2/3) + `tier_rationale` — groups the Companies section into an account plan (pursue now / nurture / monitor). Tiering rubric: research-framework.md "Account tiering".
- `competitive_context.battlecard` — per-competitor entries (claim, quoted evidence, source_url, counter_angle). **These are new factual claims and get verified like prospects**; a failed entry is dropped from the report, and entries no prospect corroborates are badged Single-source.

You don't need to hold the full schema in memory: draft the JSON, then run `python3 <skill_dir>/scripts/finalize.py --validate-only analysis.json` — it machine-checks every required field, dimension set, stage value, URL shape, and score-vs-dimensions arithmetic, and prints exactly what to fix.

## Workflow

### 1. Understand the product

- Inspect the supplied URL, repository, landing-page copy, or product description using `webfetch` or `playwright_browser_*`.
- Identify the product, outcome, buyer, user, price or buying motion, geography, and strongest use case.
- Define one primary ICP, one adjacent ICP, pain triggers, positive signals, and disqualifiers.
- Map the competitive landscape: who are the 3-5 products prospects likely already use.
- Infer missing context when safe and label the inference. Ask one concise question only when ambiguity would materially change the search.
- Log every inference in the `limits` array so the user knows what was assumed.
- If the product has zero paying customers yet (pre-launch, pre-revenue, or stated directly by the user), apply [references/research-framework.md#zero-sales-priority-mode](references/research-framework.md#zero-sales-priority-mode) for the rest of the run — it changes how Individuals are weighted and what the seven-day plan should lead with. This applies to any product category, not a specific one.

### 2. Build a public-signal search plan

Before writing generic queries, check [references/query-packs/](references/query-packs/README.md) for a pack matching the product's vertical (devtools, health/wellness, marketplace/SaaS) and start from its tuned buckets and source mix instead of the generic list below. Still cover anything a pack doesn't address using the generic buckets.

If `outcomes.jsonl` exists from a prior run on this product (see step 7), run `python3 <skill_dir>/scripts/recalibrate.py outcomes.jsonl` first and weight this run's queries toward the source types and buckets it flags as outperforming.

Search current public sources for:

- Explicit tool or alternative requests
- First-person descriptions of the target problem
- Manual workflows and repeated workaround complaints
- Migration, churn, or competitor-frustration signals
- Public company changes that create timing, such as hiring, launching, expanding, or adopting a relevant workflow
- Competitor switching signals: cancellation posts, migration threads, feature-gap complaints
- Budget and procurement signals: "justify the spend," "need ROI," "looking for free alternative"

Use `websearch` with multiple query angles and source types. Prefer original pages over search snippets. For each result, use `webfetch` to read the full page and extract evidence. Record the source URL, source type, publication date when visible, and the exact evidence supporting qualification.

**Record every query issued** in `search_queries_used` and every source visited in `sources_consulted`. This creates an audit trail.

### 3. Research safely

- Use public, intentionally shared professional or business information only.
- Do not bypass login walls, paywalls, access controls, rate limits, or robots restrictions. This governs your own searching and reading. `verify_sources.py` has its own fetch rules (no `robots.txt` handling, Reddit via `old.reddit.com`, archived copies when the live page fails); COMPLIANCE.md describes them.
- Do not use data brokers, leaked datasets, private groups, personal email discovery, phone enrichment, or sensitive personal information — this applies identically to Company prospects. A "contact path" for a company must be a public, self-serve channel (developer platform signup, partnerships page, published BD contact) — never a scraped executive's personal email or an inferred direct line.
- Do not infer protected traits or target people using health, financial hardship, political belief, sexuality, religion, or other sensitive attributes.
- Prefer companies, public professional profiles, public requests, and community posts relevant to the product.
- Quote minimally and paraphrase by default. Link every material pain or timing signal.

### 4. Classify, qualify, and deduplicate

For each candidate, classify as Individual, Segment, or Company using the test in the table above, then score using the matching dimension set (see [references/research-framework.md](references/research-framework.md)):

- **Individual:** pain strength, product fit, timing, reachability, evidence quality.
- **Segment:** pain strength, product fit, timing, evidence quality.
- **Company:** strategic fit, timing, execution ease, evidence quality.

Remove duplicates and weak matches. A prospect without a cited pain, need, or timing signal is only a speculative fit and must not appear in the primary shortlist.

**Deduplication rules:**
- Same person posting in multiple threads: keep the strongest signal, note the other in evidence.
- Same company with multiple contacts: classify as Company (org-level) unless one named person is the clear entry point, in which case also list that person as an Individual and cross-reference.
- Similar pain but different industry: keep as one Segment if the job-to-be-done is identical; split if only surface-level overlap.

Never claim that a prospect is interested, has consented, or will buy. Label the output "potential customer based on public signals."

### 5. Draft the next action — never send or execute it

- **Individual:** recommend the most natural channel already associated with the source, write one opener grounded only in cited public context, and 2-3 follow-up variations for the outreach companion skill. If no public reply/DM channel exists, say so and omit the opener rather than inventing one.
- **Segment:** write a content angle (searchable, shareable, or both — see references/research-framework.md), target keywords, suggested channels, and the proof points to cite. This is a content/GTM brief, not a message to send.
- **Company:** write a BD angle (the combined value proposition — what this unlocks for both sides), the public contact path, and a concrete first ask. This is a partnership pitch, not a cold-email drip sequence.

Across all three: avoid pretending to know the person or organization, overstating familiarity, or mentioning unrelated private details. Do not send messages, submit forms, connect, follow, comment, apply to a program, or create CRM records unless the user separately requests and authorizes that action.

### 6. Produce the report

Lead with the most actionable evidence. Use this order:

1. **Verdict** — whether the startup has reachable early-customer signals.
2. **ICP** — buyer, job, trigger, and disqualifiers.
3. **Best in category** — the strongest Individual, Segment, and Company (up to three separate call-outs — do not force a single cross-type "top prospect," since a person, an audience, and a company aren't ranked on the same scale).
4. **Individuals** — people to message: source, pain signal, fit score, stage, channel, opener.
5. **Segments** — markets to target: pain pattern, fit score, content angle, keywords, channels.
6. **Companies** — partners to pitch: pain/gap, fit score, execution path, contact path, BD angle.
7. **Repeated patterns** — pains and triggers appearing across prospects of any type.
8. **Competitive context** — what prospects currently use and where this product wins.
9. **Seven-day outreach plan** — a manual, low-volume validation sequence.
10. **Research audit** — queries issued, sources consulted, and methodology notes.
11. **Limits** — missing evidence, assumptions, and classification calls that must be confirmed through real conversations.

Create a standalone HTML report unless the user explicitly requests chat-only output:

1. Write `analysis.json` following [references/report-artifact.md](references/report-artifact.md). While drafting, iterate with `python3 <skill_dir>/scripts/finalize.py --validate-only analysis.json` until it passes.
2. Run the one-shot pipeline:

   ```bash
   python3 <skill_dir>/scripts/finalize.py analysis.json --out outputs/<slug>/signal-scout-report.html
   ```

   One command runs, in order: schema validation → source verification (`verify_sources.py`, annotating tiers in place and writing `handoff.json` next to the input) → HTML report (`generate_report.py`, with New / Seen Nx / Resurfacing badges auto-detected from sibling snapshots and `outcomes.jsonl`) → `prospects.csv` for CRM import → the cross-run diff when prior snapshots exist. It prints a condensed summary: only prospects needing action, tier counts, and output paths.

3. Act on the verification tiers it reports. Verification fetches every `source_url` and checks the cited `evidence` is actually contained in the live page — the one check that catches a claim the research invented, which no self-graded `evidence_quality` score ever will (the model scoring the evidence is the model that wrote it):

   - **Verified** — substantially quoted from the page. Ship it.
   - **Paraphrased** — supported but reworded. Tighten `evidence` to text actually on the page, or note the gap in `limits`. Does not fail the run.
   - **Not on page** — the source loaded, was readable, and the claim is not in it. **Treat as fabricated until proven otherwise.** Drop the prospect or replace `evidence` with text really there. Never ship one.
   - **Broken source** — unreachable or invalid URL. Drop the prospect or find a working source.
   - **Snippet-only** — the platform blocked the fetch (e.g. Reddit, or a 429). Keep only if the evidence came from a real discovery-search snippet; disclose it in `limits`.
   - **Unverified** — too little page text to check (JS-rendered or gated). A fetch failure, not a fabrication signal; verify by hand or note it.

   When a live page can't be read (dead link, bot wall like Reddit's, or a JS-rendered shell with too little text), verification automatically retries against the Wayback Machine's archived copy before assigning a failing tier — the verification note discloses when a claim was checked against the archive. JS-rendered pages are also mined for meta descriptions and JSON-LD before being declared unreadable.

   The pipeline exits non-zero while any prospect is **Not on page** or **Broken source** — fix the JSON and re-run until it passes. It also stamps every prospect with `verified_at` (so a report opened weeks later shows its age) and flags any Individual whose `opener` invents specifics absent from its own `evidence` with `opener_grounding_note` — a caution to tighten before sending, not a failing tier.
4. Spot-check the HTML: sections rendered, badges present, no card with an empty/"N/A" field. Return a clickable absolute file link in the final response.

**Error recovery:** the pipeline's validation output names each problem (`missing field`, wrong dimension set, score/dimension mismatch, invalid URL). Fix the JSON and retry. If the report step itself fails twice, output the JSON directly and note the script issue. If every source comes back Broken and the output says a proxy is set but unused, the machine has no direct route out: re-run with `--use-proxy`. The underlying scripts (`verify_sources.py`, `generate_report.py`, `diff_reports.py`) remain individually runnable when you need just one step.

**Caching:** If the product URL was already analyzed in this session and the user asks for a refresh, re-run only the search phase. If they ask for the same product, reuse cached research and re-score only if new signals appeared.

**Storage convention (enables steps 7-8 below):** save each run's JSON at `outputs/<product-slug>/analysis-<YYYY-MM-DD>.json` (slug the product name, e.g. `outputs/acme-crm/analysis-2026-07-14.json`) instead of a single throwaway `analysis.json`, whenever the user is likely to revisit this product. This is what makes `diff_reports.py` and `recalibrate.py` useful later — a one-off `analysis.json` in a temp dir works fine for a single-shot ask, but don't use it for a product the user is actively working.

### 7. Watch mode (offer, don't assume) — and any re-run, opt-in or not

Before finalizing a report for a product that already has saved snapshots under the storage convention above — whether this is a scheduled watch-mode run or just the user asking to re-check something they researched before — run `diff_reports.py` against *all* of that product's saved snapshots, not only the immediately-previous one:

```bash
python3 <skill_dir>/scripts/diff_reports.py outputs/<slug>/analysis-*.json --outcomes outputs/<slug>/outcomes.jsonl
```

Pass every `analysis-*.json` for the product (order doesn't matter — it sorts by each file's `generated_at`), and `--outcomes` if `outputs/<slug>/outcomes.jsonl` exists. This distinguishes three things, not two: prospects genuinely never seen before (**new**), prospects that surfaced before and are surfacing again (**recurring** — flagged loudly if they already have a logged outcome, since resurfacing a `no_reply` or `not_pursued` prospect without a new angle just repeats a decision already made), and prospects that were in the last snapshot but didn't come back this time (**dropped**). Report only this — new prospects, recurring-with-an-outcome-flag, dropped prospects, growing patterns — not the full report again.

For a scheduled recurring run, offer to set this up via the `schedule` skill (e.g. weekly) — that needs explicit user opt-in since it creates a standing job. For an ad-hoc "check this again" ask outside of watch mode, just run the diff before reporting back; no opt-in needed since nothing new is being scheduled.

### 8. Close the loop with outcomes (when available)

signal-scout's scores are self-graded — there is no ground truth until someone acts on a prospect. If the user later reports what happened after outreach (via [signal-outreach](https://github.com/OrenSegal/signal-skills/tree/main/plugins/signal-outreach) or directly), log it:

```bash
python3 <skill_dir>/scripts/log_outcome.py outputs/<slug>/outcomes.jsonl \
  --name "<prospect name>" --type individual --source-type "Forum" \
  --query-bucket pain --score 82 --outcome replied --date <YYYY-MM-DD> \
  --source-url "<prospect's source_url>"
```

`--outcome` is one of `replied`, `no_reply`, `converted`, `not_pursued`. Always pass `--source-url` when logging — it's what step 7's diff uses to tell apart two different prospects who happen to share a name, instead of merging their outcomes. Do this opportunistically, not by asking the user to fill out a form — if they mention a reply or a conversion in passing, log it. On the *next* research run for the same product, step 2 already checks for this file and runs `recalibrate.py` automatically.

### 9. Portfolio mode (when the user runs multiple products)

If the user has run signal-scout against more than one product (e.g. a founder or agency with several tools, each saved per the storage convention above), offer to cross-reference them:

```bash
python3 <skill_dir>/scripts/portfolio_merge.py "outputs/<slug-a>/analysis-*.json" "outputs/<slug-b>/analysis-*.json" --out outputs/portfolio-cross-refs.json
```

Each product argument may be a single file (as before) or a glob matching every snapshot saved for that product — cross-referencing then runs against that product's full cumulative history (reusing step 7's `diff_reports.py` accumulation), not just its latest run, so a prospect that dropped out of product A's most recent snapshot still surfaces if it's currently live in product B's. It groups prospects by exact `source_url` or normalized name and reports only those appearing in 2+ products — e.g. a person, community, or company relevant to more than one product, which is worth one shared outreach conversation instead of two separate ones. It does not re-score or judge fit across products; that comparison is left to whoever reads the output. This is opt-in and only useful once 2+ product reports exist.

## Modes

Two independent axes — combine them freely.

**`--depth`** controls how much research happens:
- **quick**: up to 5 total prospects across all types. Fastest path to action.
- **standard** (default): up to 10 total prospects.
- **deep**: up to 20 total prospects, with repeated pain patterns mapped across types.

**`--focus`** controls which prospect types get emphasized (default: `all`):
- **all**: research and report all three types as the evidence supports.
- **individuals**: prioritize addressable people over segments or companies.
- **segments**: prioritize audience/demand patterns — best when the goal is content/GTM strategy, not 1:1 outreach.
- **companies**: prioritize B2B accounts and partnership targets.
- **competitor-chasers**: within any focus, specifically surface people, segments, or companies actively switching away from a named competitor.
- **design-partners**: within any focus, prioritize prospects likely to test and give feedback over immediate buyers.

`--focus` only prioritizes; `--focus companies` can still return Individuals. For output that must name no one, use the hard filter:

**`--no-people`** (or `"people": false` in `analysis.json`): required for anything public, such as a directory listing, a registry demo, or a proof page. Do not research or write Individuals, and do not name people in any other field. Then run `finalize.py analysis.json --no-people` without `--out`: it drops Individuals, redacts person names, handles, emails, and profile URLs everywhere else, and writes every output to `public/` next to the input. Publish only that folder. The MCP server applies this filter by default. A private, client-gated report keeps Individuals only until a privacy lawyer reviews it (see COMPLIANCE.md).

Use `standard` + `all` by default.

## Completeness Checklist

Machine-checked — `finalize.py` exiting zero already guarantees these; don't re-verify them by hand:
required fields and dimension sets per type, stage values, score-vs-dimensions arithmetic, valid source URLs that resolve, no opener alongside "no channel exists," segment `content_angle` / company `execution_path` + `contact_path` present, verification run with zero **Not on page** / **Broken source**, report + CSV + handoff written.

Judgment calls — verify these yourself before delivering:

- [ ] Product brief is complete (product, buyer, job, trigger, alternatives, disqualifiers).
- [ ] At least 3 search query buckets were used (explicit demand, pain, workaround, switching, timing).
- [ ] Every prospect was classified as exactly one of Individual / Segment / Company, with non-obvious calls logged in `limits`.
- [ ] Deduplication was performed (no repeat prospects, no person double-counted as their own company without cross-reference).
- [ ] Patterns are backed by 2+ prospects each.
- [ ] Competitive context identifies 3-5 real competitors.
- [ ] Research audit logs queries and sources; limits array discloses all assumptions.
- [ ] Any Individual flagged with `opener_grounding_note` had its opener tightened to what `evidence` actually supports before being reported as ready to send.
- [ ] If handing off to signal-outreach or another consumer, used `handoff.json` rather than the raw `analysis.json`, so dropped-tier prospects don't carry forward.

## Quality bar

- Link every prospect to at least one meaningful public signal.
- Prefer ten strong matches over a long generic lead list.
- Make uncertainty and stale evidence visible.
- Personalize from the source, not from invented assumptions.
- Keep outreach manual and respectful.
- Treat the shortlist as a research hypothesis, not a customer database.
- Log your research process so someone could reproduce it.
- Name the competitors so the user can validate the landscape.
- Never force a prospect into the wrong type just to keep one list tidy — a mis-typed prospect gets the wrong next action.

Relative paths in this skill (e.g., `scripts/`, `references/`) are relative to wherever this skill is installed (e.g. `~/.agents/skills/signal-scout`). Resolve `<skill_dir>` against the actual install location, not a hardcoded path.
