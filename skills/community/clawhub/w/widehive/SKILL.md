---
name: widehive
description: "WideHive — Wide Research orchestration for AutoClaw / OpenClaw agents: fan out 100+ context-isolated sub-agents over a large target list, merge programmatically with zero LLM calls, synthesize scenario-shaped reports (financial tables / academic reviews / tech matrices). Triggers: widehive, wide research, batch research, 批量调研, 大范围调研."
---

# WideHive

> A hive of agents for wide questions. — 把一个问题，交给一整个蜂巢。

Large task → split into N independent subtasks → each subtask handled by one
context-isolated sub-agent in parallel → merge with code (not LLM) → synthesize
the final report with the main model.

Use this when a research task has **≥ 20 target objects** (papers, companies,
repos, products…). With fewer than ~10 objects, just do the task directly in the
main session — the orchestration overhead is not worth it.

## Why this works (read once)

LLMs start "slacking off" once their output fills 20–50% of the context window:
they skip sentences, compress, paraphrase. WideHive sidesteps this with
divide-and-conquer: each sub-agent gets a tiny isolated context, so every output
stays short and faithful; the merge step is pure code, so aggregation adds zero
hallucination.

Credit: the strategy follows Manus Wide Research, and the divide-merge pattern
is validated by the open-source `codex_wide_research` experiment (53/53 blog
posts summarized with zero hallucinations, where single-context baselines
covered only 12–20 before stalling).

## Iron rules (violating any of these reverts you to the slacking/hallucinating baseline)

1. **One object per sub-agent.** Never batch multiple objects into one worker.
2. **Narrow worker prompts.** Give the worker only: the object, the field
   template, the output path. No task background, no history.
3. **Short worker outputs.** Template fields only; overlong output = failure,
   send back to the retry queue.
4. **Merge with code.** Run `scripts/merge_results.py`; zero LLM calls in the
   merge stage.
5. **One file per object.** `result/<slug>.json` is the checkpoint — resume
   only what is missing, never redo finished objects.

## Run directory

`widehive/<run_id>/` under the workspace (scratch/test runs may live in a
tmp directory instead):

- `plan.json` — scenario, field template, batch_size, max_output_words, max_retries, output_form; watch runs add `mode` and a `watch` block (see Watch mode)
- `targets.json` — object list (`slug`, `name`, `url`/identifier, source hint)
- `result/<slug>.json` — one file per object, written by the worker
- `merged.csv` / `merged.json` — programmatic merge output
- `report.*` — final deliverables

## Stage 1 — Plan (main session)

- Input already contains an explicit target list → skip Stage 2.
- Input is just a topic → Stage 2 is required.
- Decide scenario: `financial` / `academic` / `tech` / `custom` (infer from the
  task; ask one question if unsure).
- Write `plan.json`: scenario, `fields` (default per scenario, see below),
  `batch_size` (default 10), `max_output_words` (default 400), `max_retries`
  (default 2), `output_form`.
- Show the user a short task brief (object count, what gets extracted per
  object, rough cost scale) before fanning out. Converge before you spend.

## Stage 2 — Enumerate (topic mode only, main session)

- Run web searches to build the candidate object list (name + URL/identifier +
  one-line source hint), write `targets.json`.
- Show the full list to the user for confirmation. Only fan out after the user
  locks the list.

## Stage 3 — Fan out (batched sub-agents)

- List existing `result/` files → skip finished objects (checkpoint resume).
- Dispatch workers in waves of `batch_size`, using your platform's sub-agent
  spawning (AutoClaw / OpenClaw: `sessions_spawn`, isolated one-shot). Label:
  `WideHive·<scenario>·<NN>`. Waiting is push-based — end the turn and
  handle completion events; report progress briefly between waves.
- Failed objects (no result file / missing fields / overlong / session failure)
  go to the retry queue, at most `max_retries` rounds; still-failing objects
  are disclosed as skipped in the final report.

**Worker prompt template** (dispatch in the user's language):

```
You are a Wide Research single-object worker. Handle ONLY this one object;
do not expand scope.

Object: <name> (<url or unique identifier>)
Task:
1. Fetch first-hand info about this object. Prefer official / authoritative
   sources. Use the best web tool available on this platform (dedicated
   web-open tools first, built-in web fetch as fallback). At most 3
   searches/fetches.
2. Extract strictly per the field template. If a value cannot be verified,
   write null — never guess:
   <field list>
3. Write the result with the file-write tool to:
   <absolute path>/result/<slug>.json (UTF-8), structure:
   {"target":"<name>","fields":{...},"sources":[{"title":"...","url":"..."}],
    "fetched_at":"<today's date>"}
4. If no file-write tool is available, return the same JSON verbatim as your
   final output.

No long prose. Write the file and finish.
```

## Stage 4 — Merge (zero LLM)

```
python <skill_dir>/scripts/merge_results.py --run-dir <run_dir>
```

- Aggregates `result/*.json` → `merged.csv` + `merged.json`; validates required
  fields, URL format, and field length; prints a JSON verdict report
  (`total_targets` / `ok` / `defects` / `missing_files` / `verdict`).
- `verdict: NEEDS_RETRY` → queue defective objects back to Stage 3.
- The script's report is the single source of truth for fan-out quality —
  never eyeball-approve a result that the script flagged.

## Stage 5 — Synthesize (main session)

- Read `merged.json` (do not re-read raw pages), spot-check 2–3 objects against
  their sources.
- Deliver per scenario (user can override):
  - `financial`: CSV/Excel metric table first + compact comparison report
  - `academic`: single-page clickable HTML review (taxonomy + per-object
    traceable summaries with source links)
  - `tech`: comparison table + analysis report (decision matrix + reasoning)
  - `custom`: agree on the shape with the user
- Ship the raw `result/` directory alongside the report — per-object results
  are never truncated, always verifiable.

## Watch mode (scheduled monitoring)

A one-shot run answers a question once. Watch mode turns a target list into a
**continuously monitored feed**: on a schedule, diff against the previous run,
re-fan-out only what changed, and emit a change report.

Enable it in `plan.json`:

```json
{
  "mode": "watch",
  "watch": {
    "baseline_run": "widehive/<previous_run_id>",
    "compare_fields": ["revenue", "gross_margin", "latest_version"],
    "schedule": "0 9 * * 1"
  }
}
```

`schedule` is informational — the platform cron job owns timing; keep it
human-readable. The scheduled run flow, triggered by a cron job whose prompt is
"Run WideHive watch run <run_id>":

1. Diff first, zero LLM and zero fan-out cost:
   `python <skill_dir>/scripts/diff_results.py --baseline <prev_run_dir> --current <cur_run_dir>`
2. **No new/changed objects** → carry results forward, emit a one-paragraph
   no-change note. Total cost ≈ 0.
3. **New/changed objects exist** → fan out workers only for those slugs
   (narrow prompts as usual), copy unchanged `result/*.json` forward from the
   baseline run so the merge covers the full list, then merge and produce a
   **change report**: what changed, per field, with sources.
4. Promote the current run to baseline (update the watch pointer / run list).

**Politeness**: schedule no faster than the target sources actually update;
add jitter; respect robots and ToS. A watch that hammers its sources gets
blocked — and burns trust for the skill, the user, and the wider ecosystem.

## Multimodal objects

An object is not always a web page. The fetch ladder extends to:

- **PDF / documents** — native PDF tooling at the worker; extract per template.
- **Video** — fetch the transcript first (platform ASR / transcript tools);
  sample visual frames only when the template actually needs them. Record the
  transcript source and timestamp coverage in the result.
- **Audio** — same as video, minus frames.
- **Images** — vision-capable analysis at the worker; store the image URL plus
  the observed facts, never the image itself.

Worker prompts stay narrow: tell the worker which modality the object is and
which tool tier to try first, exactly as with fetching. If a modality cannot
be processed on the current platform, write the object with
`"error":"unsupported_modality"` instead of silently dropping it.

## Corpus (knowledge base across runs)

Every finished run is knowledge. Before answering any question about
already-researched objects, query the corpus — do not re-fan-out and do not
re-search.

Build / refresh (after every Stage 5 and every watch run):

```python
python <skill_dir>/scripts/build_corpus.py --runs-root <workspace>/widehive --out <workspace>/widehive-corpus
```

Query rules for the main session:

1. Answer strictly from `corpus.jsonl` / `corpus-index.json`; cite the run_id
   and `fetched_at` of every figure.
2. Stale beats invented: if the corpus answer is older than the user's
   freshness need, say so and offer a targeted re-run of just the affected
   objects (watch mode's diff does this automatically).
3. If the corpus lacks the requested data, say what's missing and propose the
   narrowest fan-out that would fill the gap.

## Dashboard (interactive output)

Optional Stage 5 add-on: turn `merged.json` into a self-contained interactive
dashboard — search, sort, per-object drill-down with sources, numeric bar
charts — no external dependencies, double-click to open:

```python
python <skill_dir>/scripts/build_dashboard.py --merged <run_dir>/merged.json --out <run_dir>/dashboard.html
```

## Tabular intake & write-back

For non-technical initiators, targets and results can move through tables:

- **Intake**: accept a target list as CSV/TSV (slug, name, url, …) or a
  spreadsheet / bitable table; convert to `targets.json` at Stage 1 and show
  the parsed list for confirmation as usual.
- **Write-back**: after Stage 4, append `merged.csv` rows back to the intake
  table as new columns prefixed `wh_` (or a companion sheet/table); never
  overwrite user-owned columns.
- **Schedules**: a cron prompt may point at a table whose rows changed since
  the last run — combine with watch mode's diff to monitor a living list.

## Default field templates (override freely)

- `financial`: name, ticker, revenue, net_profit, gross_margin, yoy, key_segments, risks, source_urls
- `academic`: title, authors, year, venue, research_question, method, findings, limitations, url
- `tech`: name, owner, positioning, latest_version, stars, license, activity, pros, cons, url

## Cost & concurrency discipline

- Start at `batch_size=10`; for 100+ objects ramp 5→10→15 first to probe how
  many concurrent sub-agents the platform tolerates, then go full width.
- Workers run on the default model. Cost is controlled by narrow prompts +
  short outputs, not by a bigger budget.
- **Model tiering**: enumeration and synthesis need the strong model; workers
  only produce narrow, template-shaped output, so the platform default — or a
  cheaper model where the harness supports per-worker overrides — is enough.
  Never spend strong-model budget inside a worker.
- The run directory is the single source of truth; any interruption resumes
  from `result/`.

## Failure handling & retry playbook

Work the fallback ladder in order; stop at the first success and record which
rung was used:

1. **Retry the worker unchanged** — transient infrastructure errors (LLM
   request failure, gateway timeout) are the most common case. Max
   `max_retries` rounds.
2. **Alternate source type** — official PDF → authoritative media → secondary
   source, disclosing the downgrade in the result.
3. **Alternate fetch engine** — dedicated web-open tool → built-in fetch.
4. **Field-level fallback** — if only a few deterministically fetchable fields
   are missing (e.g. one API number), the orchestrator fetches and patches the
   file directly, disclosing "patched by fallback" in the final report. If
   infrastructure failures arrive in batches, pause fan-out and check the
   platform before continuing.
5. **Disclose** — objects that exhaust the ladder are marked skipped in the
   final report. Never silently drop an object; a blocked fetch is written as
   `{"fields":{...},"error":"fetch_failed"}` so the merge script accounts
   for it.

Track retry rounds in the run dir (`retry-queue.json`; optional but
recommended for large fan-outs). Stage 4 is done only when every object
converged or every skip is disclosed.

## Prerequisites

- Required: a sub-agent spawning capability (AutoClaw / OpenClaw `sessions_spawn` or
  equivalent) with file read/write tools for workers.
- Optional: enhanced web-open tools (e.g. AutoGLM open-link) meaningfully
  improve anti-crawl fetching; the platform's built-in fetch works as fallback.
- Porting to another harness: see [`../adapters/README.md`](../adapters/README.md)
  for per-harness mappings (OpenClaw, Claude Code, codex CLI).
