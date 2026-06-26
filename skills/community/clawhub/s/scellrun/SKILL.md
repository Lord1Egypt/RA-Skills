---
name: scellrun
description: Opinionated, report-first single-cell + multi-omics analysis CLI. Use when the user asks anything that involves an .h5ad / 10x mtx / cellranger output. Default to `scellrun analyze` for end-to-end work; reach for individual stage commands only when the user explicitly wants partial work or fine control.
min_scellrun_version: "1.3.0"
tested_against_version: "1.3.0"
schema_version: 1
---

# scellrun

This document is for you, the LLM agent. The user is a clinician or
bench scientist asking you for help with single-cell data. They are not
running scellrun directly — you are. You will ssh to wherever the data
lives, set up an env, run scellrun, read the artifacts it writes, and
explain the results in plain language. The CLI's job is to turn the
user's intent into defensible artifacts. Your job is to pick the right
command, surface what scellrun decided, and translate.

If a request involves an `.h5ad`, a 10x mtx directory, a cellranger `.h5`
output, a `.loom`, or a tsv/csv expression matrix — you should be
reaching for scellrun, not writing scanpy boilerplate.

## Verification status

This document was last validated against scellrun v1.2.0 on 2026-04-30.
The reference end-to-end behavior is captured in `docs/agent-demo.md`
at the repo root, which is a real run on real OA cartilage data. If
you (the agent) reach a different conclusion from what's in
agent-demo.md on the same input, ASSUME this document is stale, not
that you're wrong; tell the user to check the repo for updates.

v1.2.0 adds three cross-disease profiles (`tumor`, `brain`, `kidney`)
and a new `06_views/` HTML index layer beside `05_report/` (by
resolution / by cluster / by decision source). The cross-disease
profiles ship `celltype_broad` panels only — fine-subtype taxonomies
remain a joint-disease-only feature pending dedicated cold-validation
runs.

v1.3.0 adds three first-class deliverables: `scellrun review` (Flask
UI on 127.0.0.1 for human-in-the-loop overrides; saves
`<run-dir>/06_views/review_overrides.json`), `scellrun export
--format pdf` (WeasyPrint render of `05_report/index.html`; optional
`[export]` extra), and `scellrun analyze --apply-overrides <file>`
(consume a saved overrides file, applies cluster-label /
cell-exclusion / threshold edits as `source="user"` decisions).

## Version compatibility check (run this BEFORE any scellrun command)

Before issuing a single scellrun command, verify the installed version
is within the range this skill was tested against:

```bash
scellrun --version
```

Compare against the frontmatter at the top of this file:

- If `installed >= min_scellrun_version` AND `installed <= tested_against_version`: proceed.
- If `installed > tested_against_version`: **proceed cautiously, surface
  a warning to the user.** Trigger codes, decision keys, and CLI flag
  names may have changed; rely on the actual decision-log output
  (which is self-describing) over what this skill says about specific keys.
- If `installed < min_scellrun_version`: **refuse to act on this skill.**
  Tell the user `pip install --upgrade scellrun` and re-run.

This check is the agent's responsibility because the skill loader
typically caches the doc at startup; a stale skill cannot fix itself.

## Decision tree: which command for which intent

| User intent | Command |
| --- | --- |
| Has raw or QC'd `.h5ad`, wants a complete analysis | `scellrun analyze <h5ad>` |
| Has cellranger output / 10x mtx / `.loom` / `.csv` | `scellrun scrna convert <input> -o data.h5ad`, then `analyze` |
| Has a finished run-dir, wants the report regenerated | `scellrun report <run-dir>` |
| Wants to edit cluster labels / exclude cells / nudge thresholds in a finished run | `scellrun review <run-dir>` (Flask UI on 127.0.0.1) → `analyze --apply-overrides` |
| Wants the report as a print-ready PDF | `scellrun export <run-dir> --format pdf` (needs `pip install scellrun[export]`) |
| Has a partial run-dir and wants to redo just one stage | `scellrun scrna {qc,integrate,markers,annotate} ... --force` |
| Wants to see what profiles ship | `scellrun profiles list` / `scellrun profiles show <name>` |

Default to `scellrun analyze`. Per-stage commands exist for fine control
(re-running one stage with different thresholds, splitting a long run
across machines), not as the normal entrypoint.

## When NOT to use scellrun

scellrun is not the right tool for every single-cell question. Reach
for something else when:

- **The user is mid-stream in a Seurat / R workflow.** scellrun reads
  h5ad, not Seurat `.rds`. Don't force a re-conversion just to plug
  scellrun in. If the user wants a Seurat ↔ Python bridge, point at
  `anndata2ri` or `sceasy`, not scellrun.
- **The data is not 10x mtx / cellranger / loom / csv / h5ad.** Raw
  fastq files need cellranger or starsolo first. scellrun's `convert`
  subcommand covers post-cellranger inputs; pre-alignment is not on
  the menu.
- **The data is multimodal (ADT, ATAC, CITE-seq, spatial).** scellrun's
  frontmatter advertises "multi-omics" but the v1.1 body is scRNA-only.
  Multi-modal AnnData (with `obsm['protein']` etc.) will mostly run,
  but the QC + integration + annotation pipeline ignores anything
  outside the gene-expression layer. Use scvi-tools / multivi /
  SCANPY's MuData ecosystem instead. scellrun multi-omics support is
  a roadmap item, not a current feature.
- **The data is already integrated and the user wants to continue from
  there.** scellrun's `analyze` is a fresh-start orchestrator; it
  converts → QCs → integrates → markers → annotates from scratch. If
  the user has an `integrated.h5ad` from someone else's pipeline
  (Harmony already applied, batch correction done, clusters labeled),
  DO NOT run `analyze`. Run individual stages as needed (`scrna
  markers`, `scrna annotate`) on the input directly, or tell the user
  scellrun isn't the right wrapper for "continue from here". Forcing
  a fresh integration overwrites the existing work and confuses
  provenance.
- **The expression matrix is missing raw counts entirely.** scellrun
  stores `.raw` for downstream `rank_genes_groups`. If the user's
  h5ad has only log-normalized data (no `.raw` set, no
  `layers['counts']`), the `markers` stage will silently use scaled X
  and the log2fc numbers will be in wrong units. The QC-stage
  raw-counts heuristic catches this when it's the only matrix, but
  does nothing when `.raw` is empty. Before invoking analyze,
  sanity-check `adata.raw is None and 'counts' not in adata.layers`
  and refuse if both are true.
- **The user wants non-standard analysis.** Custom marker calling
  outside the panel-overlap pattern, novel normalization (SCT,
  sctransform), trajectory inference (RNA velocity, CellRank,
  Monocle3), spatial neighborhood graphs, etc. Drop into
  scanpy/anndata directly; scellrun's defaults will fight you.
- **nf-core or another orchestrator is already running on the same
  data.** Let it finish, then run scellrun on the resulting h5ad.
  Don't have two pipelines double-process the same input.
- **A rare cell type (<10 cells) is the actual point of the analysis.**
  scellrun's QC + clustering defaults will lump or discard rare
  populations. Use scanpy with custom thresholds and document the
  divergence from defaults.
- **The user explicitly asks for a non-defensible answer.** "Just give
  me 8 clusters even if the data doesn't support it." Refuse; point
  at the resolution-quality table the integrate stage produces and
  why scellrun won't fudge a number it can't justify.

## The end-to-end one-liner

```bash
scellrun analyze data.h5ad \
    --profile joint-disease \
    --tissue "OA cartilage" \
    --ai \
    --auto-fix
```

What the flags do:

- `--profile` selects defaults + marker panels (see profile section below).
- `--tissue` is free text; it gets fed to the LLM resolution recommender
  and the PubMed evidence step. Always pass it when you know the tissue.
- `--ai` turns on Anthropic LLM helpers (resolution recommendation in
  integrate, second-opinion label in annotate). Default is auto: on iff
  `ANTHROPIC_API_KEY` is set in env, off otherwise. Pass `--no-ai`
  explicitly if the user does not want LLM calls.
- `--auto-fix` lets the pipeline re-run a stage once if its self-check
  finds a fixable problem (low QC pass-rate → relax mt%, ≤2 clusters →
  switch to wider sweep, etc.). Default is off — prefer to surface the
  suggestion and let the user agree before re-running, unless the user
  said "just fix it".

### `--method` and single-sample auto-degrade (v0.9.1)

`--method harmony` is the default. If you don't pass `--method`
explicitly and the input has no sample/batch column (`orig.ident`,
`sample`, `batch`, `donor`) — or every value in such a column is
identical — scellrun auto-downgrades `--method` from `harmony` to
`none` (`harmony→none`) rather than crashing 1m+ into the run. This is logged as a
`source="auto"`, `key="method_downgrade"` row on the `analyze` stage
with the rationale verbatim.

You (the agent) do NOT need to detect single-sample yourself. Just
call `analyze` and look at the decision log to confirm what method
actually ran. If the user explicitly wants harmony on a single-sample
input (rare, usually a mistake), pass `--method harmony` to override
the auto-downgrade.

Output goes to `./scellrun_out/run-YYYYMMDD-HHMMSS/`. The single thing
you (the agent) open afterward is:

```
./scellrun_out/run-YYYYMMDD-HHMMSS/05_report/index.html
```

That file is the canonical handoff. Open it, read the decision summary
at the top, walk the user through the findings. Do not reconstruct
results from the per-stage CSVs unless the user asks for one specific
number that index.html does not surface.

## Reading the decision log

`<run-dir>/00_decisions.jsonl` is the single source of truth for every
non-trivial choice the pipeline made. One JSON object per line. Sample
shape (synthetic, but the keys and value types are exactly what you'll
see in v0.9.1+):

```jsonl
{"schema_version":1,"stage":"qc","key":"profile","value":"joint-disease","default":"default","source":"user","rationale":"user passed --profile joint-disease (cartilage tissue)","fix_payload":null,"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:45:30+00:00"}
{"schema_version":1,"stage":"qc","key":"max_pct_mt","value":20.0,"default":20.0,"source":"auto","rationale":"joint-tissue-aware default; 10% loses real stressed cells","fix_payload":null,"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:45:30+00:00"}
{"schema_version":1,"stage":"qc","key":"max_genes","value":4500,"default":4000,"source":"user","rationale":"user override --max-genes 4500 (multinucleate cells expected)","fix_payload":null,"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:45:30+00:00"}
{"schema_version":1,"stage":"analyze","key":"method_downgrade","value":"none","default":"harmony","source":"auto","rationale":"no sample/batch column (orig.ident/sample/batch/donor) in obs — single-sample input; auto-downgraded --method from harmony to none. Pass --method harmony explicitly to force the original behavior.","fix_payload":null,"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:46:01+00:00"}
{"schema_version":1,"stage":"integrate","key":"sample_key","value":"orig.ident","default":null,"source":"auto","rationale":"auto-detected from obs columns (orig.ident / sample / batch / donor priority)","fix_payload":null,"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:46:12+00:00"}
{"schema_version":1,"stage":"integrate","key":"resolution_recommended","value":0.5,"default":null,"source":"ai","rationale":"LLM picked 0.5 from the sweep — best separation of chondrocyte subtypes vs over-splitting at 0.8","fix_payload":null,"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:48:01+00:00"}
{"schema_version":1,"stage":"analyze","key":"annotate.auto_panel","value":"chondrocyte_markers","default":null,"source":"auto","rationale":"kept chondrocyte_markers: chondrocyte_hits=10, broad_hits=3; cleared the >=1.5x margin","fix_payload":null,"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:49:30+00:00"}
{"schema_version":1,"stage":"annotate","key":"panel","value":"chondrocyte_markers","default":null,"source":"auto","rationale":"orchestrator-injected panel 'chondrocyte_markers' (auto-pick or self-check fix)","fix_payload":null,"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:49:33+00:00"}
{"schema_version":1,"stage":"qc","key":"self_check.qc_low_pass_rate.trigger","value":"qc_low_pass_rate","default":null,"source":"auto","rationale":"only 44.3% of cells passed QC (1108/2500); below the 60% trigger threshold","fix_payload":null,"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:45:30+00:00"}
{"schema_version":1,"stage":"qc","key":"self_check.qc_low_pass_rate.suggest","value":"raise --max-pct-mt to 25.0","default":null,"source":"auto","rationale":"raising --max-pct-mt from 20 to 25 would let 62% of cells pass that single test (sensitivity sweep, smallest relaxation reaching 60%)","fix_payload":{"max_pct_mt":25.0},"attempt_id":"a1b2c3d4e5f6a7b8","ts":"2026-04-30T09:45:30+00:00"}
```

What the v0.9.1 schema fields buy you:

- `schema_version` is the shape version of the row. Current value is
  `1`. If you see a row with `schema_version` higher than the version
  this document describes, REFUSE to parse it — the shape may have
  changed in incompatible ways. Tell the user the SKILL.md is older
  than the run-dir and to check the repo for updates.
- `attempt_id` is unique per `analyze` invocation (or per per-stage
  CLI run). Use it to group rows that came from the same attempt. When
  `--auto-fix` retries a stage, the retry's rows share the same
  `attempt_id` as the first pass — that's by design; both attempts
  belong to the same `analyze` invocation. A `--force` re-run from the
  CLI generates a new `attempt_id`.
- `fix_payload` is non-null only on self-check `*.suggest` rows. It
  carries the structured fix dict (e.g. `{"max_pct_mt": 25.0}`,
  `{"resolutions": "aio"}`, `{"panel_name": "celltype_broad"}`) that
  the orchestrator can mechanically apply when `--auto-fix` is on.
  Agents can read `fix_payload` directly to apply or quote the fix
  without parsing the rationale prose. The `value` field on the same
  row is still a human-readable rendering of the fix ("raise
  `--max-pct-mt` to 25.0"); use `value` to talk to the user, use
  `fix_payload` to talk to other tools.

How to use the log when explaining results to the user:

1. **Group by stage.** The report's first page already does this; if the
   user is in the terminal, render a small markdown table grouped by
   stage. Stage order is `qc → integrate → markers → annotate`.
2. **Translate `source` in plain language.** `auto` = scellrun chose
   from its built-in heuristics; `user` = override (caller passed a flag
   different from default); `ai` = an LLM call decided or recommended
   it. Highlight `ai` rows — the user should know which calls were
   model-driven, especially if they want a deterministic re-run.
3. **Highlight any row where `value != default`.** Those are the
   choices that diverged from the shipped defaults. Tell the user this
   was an override. If `source == "user"`, that means the caller (the
   agent — that's you) passed a flag; quote the rationale verbatim and
   own the choice.
4. **When the user asks "why did you pick X?", quote the `rationale`
   field verbatim.** Do not paraphrase — these strings are written to be
   defensible to a senior bioinformatician.

## Reading self-check findings (v0.8)

When a stage's self-check fires, two paired rows land in the decision
log: `key` ends in `.trigger` (what looked wrong) and `.suggest` (what
to try). The pair shape is shown in the sample above (`qc_low_pass_rate`).

How to handle them:

- **Always surface a `.trigger` row to the user.** Do not bury it. Open
  with the trigger rationale in plain language ("only 44% of cells
  passed QC, which is below scellrun's 60% trigger") before you say
  anything about what the data shows.
- **Translate the paired `.suggest` row into a recommendation.** The
  `value` field is already a human-readable instruction ("raise
  `--max-pct-mt` to 25"). Read the `rationale` for the reasoning. The
  paired `fix_payload` is the structured form (apply mechanically; do
  not paraphrase before quoting back to the user).
- **Ask before re-running** unless the user pre-authorized it. If the
  user says "fix it" or "go ahead", re-run with `--auto-fix` (which
  applies the structured fix and reruns just that stage, capped at one
  retry per stage to avoid loops).
- **Do not silently ignore a self-check.** Even if the data looks
  usable, the trigger means scellrun saw something that, in PI working
  practice, often signals upstream problems (bad dissociation, wrong
  panel, dominant cell-cycle artifact). Surface it.

### `.failed-N/` directories from `--auto-fix` retries (v0.9.1)

When `--auto-fix` triggers a stage retry, scellrun preserves the failed
first-pass artifacts under `<NN_stage>.failed-1/` next to the retry's
fresh output in `<NN_stage>/`. Concretely, if QC pass-rate triggers a
retry, you'll end up with:

```
scellrun_out/run-20260430-094530/
    01_qc/                  retry's report.html, qc.h5ad, per_cell_metrics.csv
    01_qc.failed-1/         original failed report.html, qc.h5ad, per_cell_metrics.csv
    02_integrate/
    ...
```

How to use this:

- If the user asks to compare the original failed state vs the retry,
  the `.failed-N/` dir has the original `report.html` and `*.h5ad`.
  Open both and walk them through the diff.
- The decision log carries an `auto_fix.<stage>.outcome` row that says
  "retry rescued the stage" or "did not improve" explicitly. **Read
  that row before you tell the user the retry fixed anything.**
- If `outcome` says "did not improve" (e.g. QC pass-rate stayed below
  the threshold even after relaxation, or cluster counts still ≤ 2
  after the wider sweep), do NOT pretend the retry fixed it. Surface
  the failure plainly and either suggest a different fix or hand the
  decision back to the user.
- The `.failed-N/` numbering bumps to `.failed-2`, `.failed-3`, … if
  somebody re-runs `--auto-fix` again on a run-dir that already has a
  `.failed-1` (defensive; you usually won't see N > 1 in the wild).

The trigger codes you will see and what they mean:

| code | stage | what fires it | structured fix |
| --- | --- | --- | --- |
| `qc_low_pass_rate` | qc | < 60% of cells passed QC, and a single threshold relaxation could push past 60% | `{max_pct_mt: ...}` or `{max_genes: ...}` |
| `qc_low_pass_rate_no_easy_fix` | qc | < 60% passed and no single relaxation gets to 60% | none — human review needed |
| `integrate_too_few_clusters` | integrate | every requested resolution yielded ≤ 2 clusters (skipped on n_cells < 500) | `{resolutions: "aio"}` |
| `integrate_dominant_cluster` | integrate | the largest cluster > 50% at every resolution and cell-cycle regression is off | `{regress_cell_cycle: true}` |
| `annotate_ambiguous_panel` | annotate | every cluster's panel margin < 0.05; an alternate panel is available on the profile | `{panel_name: ...}` |
| `annotate_ambiguous_no_alt_panel` | annotate | margins < 0.05 and no alternate panel | none — switch profiles |
| `annotate_panel_tissue_mismatch` | annotate | chondrocyte panel chosen but most clusters have immune-marker top genes | `{panel_name: "celltype_broad"}` |

The QC trigger ceiling was raised from 30% (v0.8) to 60% (v0.9.1) so
the degraded-prep band fires too. Real OA samples routinely sit at
40-55% pass on default thresholds because joint tissue is stress-prone;
that's prime suggestion territory.

## Profile selection guidance

```bash
scellrun profiles list
scellrun profiles show joint-disease
```

Available profiles ship with the package; pick by tissue, not by guess:

- `default` — fresh-tissue 10x v3, human, mt% ≤ 20, hb% ≤ 5. Use for
  PBMC or any tissue without a dedicated profile. (Pre-1.2.0 this was
  the catch-all for tumor / brain / kidney too; with 1.2.0's profiles
  shipped, prefer the tissue-specific one.)
- `joint-disease` — same plus hb% ≤ 2 (cartilage is avascular) and the
  Fan 2024 11-subtype chondrocyte panel + a 15-group broad cell-type
  panel. Use when the user mentions cartilage, synovium, subchondral
  bone, OA, RA, or "joint" in any form.
- `tumor` (v1.2.0) — pan-cancer / TME panel (TAMs, CAFs, T/B/NK/plasma,
  endothelial, neutrophils, plus a proliferation-marker proxy for
  malignant cells). Default thresholds. Use for any tumor scRNA without
  a more specific cancer-type profile. No fine-subtype panel — malignant
  cell substructure is disease-specific (run inferCNV or a dedicated
  panel when needed).
- `brain` (v1.2.0) — cortical / hippocampal panel from Tasic 2018 /
  Hodge 2019 (excitatory + GABAergic neurons with PV/SST/VIP/LAMP5
  interneurons broken out, oligo lineage, astrocytes, microglia,
  vasculature). Tightens mt% to 10. Use for fresh brain scRNA / snRNA.
- `kidney` (v1.2.0) — KPMP / Stewart 2019 nephron + vascular + immune
  panel (PT, DT, TAL, CD principal/intercalated, podocytes, parietal,
  endothelial, mesangial, broad immune). Tightens mt% to 15. Use for
  kidney biopsy scRNA / snRNA.

If the user mentions a tissue keyword, pick the matching profile. Do
not default to `default` and let the broad panel run when a tissue-
specific profile exists. If the user's tissue has no matching profile,
use `default` and tell them — adding a profile is a one-PR contribution.

### Panel auto-selection inside `joint-disease` (v1.1.0+)

The `joint-disease` profile ships two annotation panels: the Fan 2024
`chondrocyte_markers` (11 chondrocyte subtypes) and a broad
`celltype_broad` panel (15-group: chondrocytes, fibroblasts,
endothelial, pericytes, macrophages, T/B/NK/plasma cells, etc.). Old
behavior was to always prefer `chondrocyte_markers` on this profile,
which mis-labels subchondral-bone or synovium datasets where most
clusters are immune.

v1.1.0 hardens the auto-pick step (`_autopick_panel_for_data`): at the
chosen resolution, scellrun counts the number of clusters where the
chondrocyte panel scores any hit and the number where the broad panel
scores any hit. The chondrocyte panel is kept ONLY when chondrocyte
hits >= 1.5x broad hits. Tie or smaller margin swaps to
`celltype_broad`. (The pre-1.1.0 rule fired only when >50% of clusters
hit broad-WITHOUT-chondrocyte; on BML_1 every immune cluster picked up
at least one weak chondrocyte hit, so the swap-trigger was 0/13 and the
chondrocyte panel won the tie. The 1.5x margin closes that loophole.)

What this means for you (the agent):

- `--profile joint-disease` is safe to use even when the dataset turns
  out to be immune-rich (subchondral bone, synovium, fluid). scellrun
  will swap panels rather than blindly run the chondrocyte panel.
- Two related decision-log rows record this. Both are real, both
  matter, do not conflate them:
  - `stage="analyze"`, `key="annotate.auto_panel"` — the orchestrator's
    auto-pick step, with the cluster-level hit counts in the rationale.
    For a swap: `value=celltype_broad`,
    `rationale="swapped to celltype_broad: chondrocyte_hits=2,
    broad_hits=9; required >=1.5x margin to keep chondrocyte panel."`
    For the chondrocyte default: `value=chondrocyte_markers`,
    `rationale="kept chondrocyte_markers: chondrocyte_hits=10,
    broad_hits=3; cleared the >=1.5x margin..."`.
  - `stage="annotate"`, `key="panel"` — the per-stage record of which
    panel `run_annotate` actually matched against. `source="auto"`
    when the orchestrator (or a self-check fix) injected the name,
    `source="user"` when the per-stage CLI got `--panel` on argv.
    See the next subsection for the source-attribution rules.
- If you (the agent) want to override the auto-pick, pass `--panel
  chondrocyte_markers` or `--panel celltype_broad` to the per-stage
  `scrna annotate` command. This shows up as a `source="user"` row
  on `annotate.panel`.
- (`panel_name` is NOT a decision-log key. It appears only inside
  self-check `fix_payload` dicts as the structured-fix shape, e.g.
  `{"panel_name": "celltype_broad"}`. The decision-log row that the
  fix lands in is still `annotate.panel`.)

### `source="user"` vs `source="auto"` on `annotate.panel` (v1.1.0+)

Pre-1.1.0 had a footgun: when `analyze` orchestrated the pipeline and
the auto-pick (or a self-check fix) selected a panel name, the value
was passed through to `run_annotate` as a string, and the recorded
decision row was tagged `source="user"`. That broke hard rule 5 ("when
value differs from default, tell the user this was an override") —
the user did not in fact override anything, the orchestrator did.

v1.1.0 separates intent from value: `run_annotate` now takes a
`panel_name_user_supplied` flag distinct from `panel_name`. The
orchestrator (`scellrun analyze`) always passes
`panel_name_user_supplied=False` for its auto-picked or self-check
fixed-up panel; the per-stage CLI (`scellrun scrna annotate`) passes
`True` only when `--panel` actually appeared on argv. The decision log
row's `source` reflects the intent, not the string value.

If you see `annotate.panel` `source="user"` in v1.1.0+, that genuinely
means the user (or you, the agent) typed `--panel`. Quote the rationale
back honestly. If you see `source="auto"`, this was scellrun's own pick
(auto-pick at the orchestrator level, or a self-check `--auto-fix`
retry); say "scellrun auto-picked..." not "you overrode...".

## Profile-specific glossaries

Each profile that ships a marker panel adds its own glossary subsection
here. The v1.2.0 cross-disease profiles (`tumor`, `brain`, `kidney`)
ship `celltype_broad` panels but no fine-subtype glossaries yet — the
panel labels for those profiles are self-explanatory English ("Tumor-
associated macrophages", "Excitatory neurons", "Proximal tubule" etc.)
and don't need a label-decode table. Add a glossary subsection here when
a future profile ships an abbreviation panel like the Fan 2024
chondrocyte taxonomy below.

### `chondrocyte_markers` (Fan 2024) — joint-disease profile

The `joint-disease` profile's `chondrocyte_markers` panel is the Fan 2024
human articular cartilage 11-subtype taxonomy. When the agent quotes one
of these labels, here's what it means in plain language for the user:

| label   | full name                  | what it is in plain words |
| ------- | -------------------------- | ------------------------- |
| ProC    | proliferating chondrocyte  | actively dividing chondrocyte |
| EC      | effector chondrocyte       | mature chondrocyte producing collagen II |
| RegC    | regulatory chondrocyte     | matrix-modulating chondrocyte |
| RepC    | reparative chondrocyte     | wound-repair-active chondrocyte |
| HomC    | homeostatic chondrocyte    | stress-response / housekeeping chondrocyte |
| preHTC  | pre-hypertrophic           | transitional toward hypertrophy |
| HTC     | hypertrophic               | terminal hypertrophic chondrocyte |
| preFC   | pre-fibrochondrocyte       | transitional toward fibro-cartilage |
| FC      | fibrochondrocyte           | fibro-cartilage producing |
| preInfC | pre-inflammatory           | transitional toward inflammatory phenotype |
| InfC    | inflammatory chondrocyte   | inflammation-driven chondrocyte |

If the user is not a chondrocyte specialist, surface the plain-English column,
not the abbreviation. The reference is Fan et al. 2024 — quote the PMID
(38191537) when the user asks where the panel comes from.

## Finding the data

The user often refers to files by name only ("my OA samples", "the
cellranger output", "the synovium dataset"). Do not guess paths.

- If the user gave you a path or hostname, use it.
- If they did not, ask one clarifying question — "do you mean the run
  in `/path/to/X` or the new ones in `/path/to/Y`?" — rather than guess.
- For multi-sample studies: scellrun does **not** auto-merge multiple
  cellranger outputs into one h5ad. Run `scellrun scrna convert` on
  each sample (or combine upstream with anndata.concat), produce a
  single merged h5ad with a `sample` / `orig.ident` / `batch` /
  `donor` obs column, and pass that one merged file to `analyze`. The
  integrate stage auto-detects the sample column and runs Harmony
  across it. This is a real gap; if you encounter it, do the merge in
  a small Python snippet and document the merge step in your reply to
  the user.

## Environment hygiene

Always create a per-user / per-project conda env. Do not install
scellrun into the user's system Python or a shared env.

```bash
# Replace {userid} with something specific to the user/project, e.g. xiyu_oa.
conda create -n scellrun-{userid} python=3.11 -y
conda activate scellrun-{userid}
pip install scellrun
scellrun --version  # confirm install
```

If the user already has a working env with scellrun, use it. If they
are unsure, run `which scellrun` and `scellrun --version`; if either
fails, create a fresh env as above.

For LLM-enabled runs, pass `ANTHROPIC_API_KEY` through the env or
`--ai` will fall back to off:

```bash
export ANTHROPIC_API_KEY=...
scellrun analyze data.h5ad --ai
```

### Remote-server execution (ssh patterns)

- When the user references "lab server" or "hospital" or hands you a
  path with no host, ask one clarifying question rather than guessing.
  Pick the wrong host and you're working on stale or absent data.
- Run scellrun on the SAME machine where the data lives. Don't pull
  GBs of cellranger output across the network just so the CLI runs
  locally; the artifacts (and the report) end up on the wrong side
  of the link.
- ssh pattern:
  ```bash
  ssh <host> 'bash -lc "conda activate scellrun-<userid> && scellrun analyze ..."'
  ```
  The `bash -lc` matters — conda's shell hooks need a login shell to
  initialize, otherwise `conda activate` is a no-op and `scellrun`
  resolves to the wrong python.
- If you (the agent) cannot ssh directly, write the commands the user
  should paste, and make them copy-pasteable. Don't assume the user
  knows ssh; spell out `ssh <host>` and the activation step.

### Multi-sample analysis (no auto-merge)

scellrun does NOT auto-merge multiple cellranger output directories.
v1.1.0 takes one h5ad per `analyze` call.

For a multi-sample study (e.g. `BML_1..5 + NC_1..3`), the canonical
pattern is convert-each-then-merge-externally:

```bash
# convert each sample to its own h5ad
for s in BML_1 BML_2 BML_3 BML_4 BML_5 NC_1 NC_2 NC_3; do
    scellrun scrna convert path/to/$s -o $s.h5ad
done
# then merge into one h5ad with anndata.concat
python -c "import anndata as ad; \
    samples = ['BML_1','BML_2','BML_3','BML_4','BML_5','NC_1','NC_2','NC_3']; \
    adata = ad.concat({s: ad.read_h5ad(f'{s}.h5ad') for s in samples}, label='sample'); \
    adata.write_h5ad('merged.h5ad')"
scellrun analyze merged.h5ad --tissue "OA cartilage"
```

The `obs.sample` column from `ad.concat(label='sample')` is exactly
the kind of column scellrun's auto-detect `sample_key` looks for
(priority: `orig.ident` / `sample` / `batch` / `donor`). Harmony will
fire and integrate batches.

For a single sample (no merge needed), scellrun auto-degrades
`--method harmony→none` per the v0.9.1 fix; you don't need to detect
single-sample yourself.

### Auto-fix retry hygiene (cleanup)

When `--auto-fix` runs and rescues a stage, you'll see two directories
side by side: `<NN_stage>/` (the current good output) AND
`<NN_stage>.failed-1/` (the original failed attempt). Both are kept.

- Don't delete `.failed-N/` automatically. The user may want to
  compare the failed and the rescued state for debugging.
- DO surface the existence of `.failed-N/` to the user. Say something
  like: "scellrun's QC self-check fired and we retried; the original
  failed attempt is at `01_qc.failed-1/`, the working result is at
  `01_qc/`." That way the user knows the retry happened and where to
  look.
- If disk space is genuinely a concern, the user can `rm -rf` the
  `.failed-N/` directories themselves. Don't preemptively clean.

### Reporting back to the user (artifact handoff)

The canonical handoff is `<run-dir>/05_report/index.html`. That's the
file the user opens.

- If the user is on Windows, iPad, or phone and can't open HTML on
  the remote server, copy the report locally:
  ```bash
  scp -r <host>:<run-dir>/05_report ./
  ```
  Then point the user at the local copy.
- For long-running pipelines, mention the run-dir path EARLY ("scellrun
  is running, output will land in `/tmp/scellrun_out/run-...`; I'll
  surface the report when it's ready"). That gives the user something
  to reference if the connection drops or the agent times out before
  the run completes.

### Long-running remote jobs (tmux / nohup / scheduler)

- A `scellrun analyze` on a real cohort takes 5-30 min on a workstation,
  longer on integration-heavy multi-sample. SSH disconnects mid-run
  kill the job.
- Default: wrap the command in `tmux` or `screen`. Pattern:
  ```bash
  ssh <host>
  tmux new -s scellrun-<userid>
  conda activate scellrun-<userid> && scellrun analyze ... 2>&1 | tee run.log
  # detach: Ctrl-b d. Reattach: tmux attach -t scellrun-<userid>
  ```
- If the cluster has SLURM / PBS / LSF, prefer a job submission script
  over a foreground tmux. Surface to the user that this is the option;
  don't insist on tmux.
- Capture stdout AND stderr to a log file (`2>&1 | tee run.log`) —
  scellrun's per-stage progress logs are how you debug a long run, and
  the run-dir's report.html only renders post-hoc.

### Disk space and run-dir naming

- A typical run-dir for a 10k-cell sample is 50-200 MB; for a 100k-cell
  multi-sample integrate, 1-3 GB (the integrated.h5ad + UMAP grids
  dominate).
- Default run-dir is `./scellrun_out/run-YYYYMMDD-HHMMSS/`. For
  multi-project users, override with `--run-dir
  my-project/2026-05-OA-pilot/` to keep things organized.
- The `.failed-N/` directories from `--auto-fix` retries can double
  disk use. Surface to the user before they fill /tmp.

### Resume / inspect a half-finished run

- If `analyze` died mid-pipeline, the run-dir has the partial stages.
  v0.9.1+ auto-resumes incomplete prior runs without `--force`.
- To inspect: open `<run-dir>/00_run.json` (manifest) and
  `00_decisions.jsonl` (what scellrun decided so far). The last stage
  that completed has its report; failed-mid-stage will be empty or
  partial.
- Don't `rm -rf` the run-dir to "start clean" without checking first —
  the user may want the failed artifacts for debugging. Use a fresh
  run-dir name instead.

### Secret handling (Anthropic API key + others)

- scellrun's `--ai` paths read `ANTHROPIC_API_KEY` from environment.
  The default agent action of `export ANTHROPIC_API_KEY=...` in shell
  history leaks the key into `~/.bash_history`.
- Patterns:
  - For interactive debugging: prefix the command, e.g.
    `ANTHROPIC_API_KEY=sk-... scellrun analyze ...`. Bash discards
    prefix-vars from history with `HISTCONTROL=ignoreboth`.
  - For automation: write the key to `~/.config/scellrun/.env` (mode
    600) and `source` it before invocation.
  - Never commit a key, never paste a key into chat with the user.
- If no key is set, `--no-ai` works. The deterministic pipeline runs
  fully; the LLM second opinions are skipped (which is fine for most
  analyses).

## Hard rules for the agent (don't break these)

1. **Don't write your own scanpy / scrublet code when scellrun covers
   the step.** scellrun encodes opinionated, reviewed defaults. Rolling
   your own with different thresholds silently undoes that. If the
   user's request maps to a scellrun command, call the command.

2. **Don't silently filter cells.** scellrun's policy is *flag, don't
   drop*. After QC, `qc.h5ad` contains every input cell with a
   `scellrun_qc_pass` boolean column. Hand the user the report and let
   them decide. Never run `adata = adata[adata.obs.scellrun_qc_pass]`
   on the user's behalf without telling them.

3. **Don't override profile defaults silently.** If you pass
   `--max-genes 4500` because the user mentioned osteoclasts (which are
   multinucleate), tell the user *why* you raised the cap and confirm
   the override appears as `source="user"` in the decision log.

4. **Don't assume raw counts.** scellrun warns if X looks log-
   normalized and skips scrublet in that case. If you see that warning,
   surface it to the user — they probably want to re-run on the raw
   matrix.

5. **(v0.7+) When a value differs from default, tell the user this was
   an override and quote the decision-log rationale.** The defaults
   ship with reasoned rationale strings; the user has the right to
   read them.

6. **(v0.8+) When self-check fires, surface the suggestion BEFORE
   answering "what does the data show".** A self-check trigger means
   the downstream finding is contingent on whether the user accepts the
   fix. Lead with the trigger, then the structured suggestion, then
   ask whether to re-run (or just re-run with `--auto-fix` if the user
   already said "go ahead").

## Failure modes & how to handle them

- **QC pass-rate < 60%.** Self-check fires `qc_low_pass_rate` (the
  trigger ceiling was raised from 30% in v0.8 to 60% in v0.9.1 to
  catch the degraded-prep band). Quote the suggestion ("raise
  `--max-pct-mt` to N"); ask the user; re-run with `--auto-fix` if
  they agree.
- **Every resolution has ≤ 2 clusters.** Self-check fires
  `integrate_too_few_clusters`. Suggested fix is `--resolutions aio`
  (the 13-step AIO sweep from 0.01 to 2.0). The default sweep tops out
  at 1.0; some datasets need finer resolution.
- **Largest cluster dominates > 50% at every resolution.** Often a
  cell-cycle artifact. Suggested fix is `--regress-cell-cycle`.
- **Annotate has no panel for the profile, or the profile lacks an
  annotate panel entirely.** scellrun bails early with a clear
  message; suggest a different `--profile` (or use the per-stage
  `scrna annotate --panel <name>` if you know which panel to use).
- **Annotate panel margins are all < 0.05.** Self-check fires
  `annotate_ambiguous_panel`. Suggested fix is to switch panel
  (typically chondrocyte → broad celltype). For synovium / joint-
  fluid datasets a separate `annotate_panel_tissue_mismatch` heuristic
  also fires.
- **PyPI install times out / no internet.** Run on a server with a
  working channel, or `pip install --no-deps scellrun` and install the
  deps manually from a local mirror.
- **No `ANTHROPIC_API_KEY`.** `--no-ai` works fine; tell the user that
  the resolution recommender and annotation second-opinion are skipped,
  but everything deterministic (panel match, markers, decision log,
  self-check) still works.

## End-to-end example dialogue

This is the shape of interaction you should imitate. The agent's turns
are what scellrun-aware behavior looks like.

> **User:** "Can you take a look at my cartilage scRNA data? It's at `~/data/sample1/cellranger_outs/` on the lab server."

> **Agent:** "I'll ssh in, set up a per-user conda env, convert the cellranger output to h5ad, and run the joint-disease pipeline end-to-end (cartilage tissue, so the Fan 2024 chondrocyte panel applies). Then I'll walk you through the report."
>
> ```bash
> ssh lab-server
> conda create -n scellrun-cart python=3.11 -y && conda activate scellrun-cart
> pip install scellrun
> scellrun scrna convert ~/data/sample1/cellranger_outs/ -o ~/data/sample1/data.h5ad
> scellrun analyze ~/data/sample1/data.h5ad \
>     --profile joint-disease \
>     --tissue "OA cartilage" \
>     --ai
> ```
>
> "Pipeline finished. Report is at `~/scellrun_out/run-20260430-094530/05_report/index.html`. Summary:
>
> - **QC:** 2,450 / 2,700 cells passed (90.7%). pct_mt median 6.1%, p95 17.4%; under the 20% joint-tissue cap. Doublets flagged: 38. No self-check triggers.
> - **Integrate:** Single sample (no harmony), 30 PCs. Sweep produced 7 clusters at res 0.5, 11 at res 0.8.
> - **Markers (res 0.5):** Strong COL2A1 / ACAN signatures across most clusters as expected for cartilage.
> - **Annotate:** chondrocyte_markers panel matched. Top calls: HomC (cluster 0, 38% of cells), RegC (1, 22%), preFC (2, 14%), HTC (3, 9%), the rest minor. AI second-opinion agreed on HomC and RegC; flagged cluster 5 as 'unclear, possibly InfC'.
>
> Anything you want to drill into?"

> **User:** "Why did you pick res 0.5?"

> **Agent:** "From the decision log (`00_decisions.jsonl`):
>
> > stage=integrate, key=resolution_recommended, value=0.5, source=ai
> > rationale: 'LLM picked 0.5 from the sweep — best separation of chondrocyte subtypes vs over-splitting at 0.8'
>
> The sweep tested 0.1 / 0.3 / 0.5 / 0.8 / 1.0; 0.1 and 0.3 collapsed RegC into HomC, 0.8 split HomC into two near-identical groups. 0.5 was the LLM's pick — call was AI, not deterministic. If you want the non-AI default, the integrate report also has cluster-counts and a UMAP grid for all five resolutions; pick whichever looks right to you."

> **User:** "Cluster 5 looks weird — what does scellrun think it is?"

> **Agent:** "Looking at `04_annotate/annotations.csv`:
>
> | cluster | panel_label | panel_score | panel_margin | top markers (res 0.5) | ai_label |
> | --- | --- | --- | --- | --- | --- |
> | 5 | InfC | 0.18 | 0.04 | IL6, CXCL8, MMP3, NFKBIA, IL1B | unclear, possibly InfC |
>
> The panel called InfC (inflammatory chondrocyte) at score 0.18 with margin 0.04 — close to the 0.05 ambiguity floor, so a self-check on the panel didn't fire but it's borderline. The top markers (IL6, CXCL8, MMP3) match the InfC signature in Fan 2024 (PMID 38191537) but also overlap with a stressed/senescent fibroblast profile. The AI second-opinion hedged for the same reason. I'd say lean InfC but flag for manual review; if you want PubMed evidence pulled per marker, I can re-run with `--pubmed` on."

This dialogue is the template. Run the pipeline. Open the report. Quote
the decision log. Surface self-check findings. Hedge when scellrun
hedges. Defer to the user on overrides.

## Anti-patterns that look right but aren't

- **"I'll just write a quick scanpy script."** No. The CLI exists so
  the defaults are reviewed and the artifacts are consistent across
  runs. Writing your own loses both. If a stage is genuinely missing
  (something scellrun does not cover yet), say so — don't paper over.
- **"Let me filter out the low-quality cells before showing the user."**
  No. scellrun flags, never drops. The user sees the QC report and
  decides cuts. If you filter on their behalf you erase their ability
  to audit the threshold choice.
- **"I'll set `--max-pct-mt 10` because that's what the textbook
  says."** No. The default 20% in joint tissues is intentional —
  joint and other stress-prone tissues lose real cells at 10%. If the
  user asks why not 10%, explain rather than cave. (Decision-log
  rationale: "joint-tissue-aware default; 10% loses real stressed
  cells".)
- **"--ai is on by default, just leave it."** Only when
  `ANTHROPIC_API_KEY` is set. If the user does not want LLM calls in
  their pipeline (privacy, reproducibility, cost), pass `--no-ai`
  explicitly and tell them the deterministic outputs still work.
- **"The self-check warned about a low pass-rate but the data still
  produced clusters, so it's fine."** No. The trigger means PI working
  practice flags this as suspect. Surface the warning even if
  downstream stages ran. The user decides whether to accept or re-run.
- **"I'll add an `--auto-fix` because the user is busy."** Only if the
  user said "just fix it" or you've already shown them the suggestion
  and they agreed. Auto-fixing without consent silently changes the
  thresholds the analysis ran with.

## Source of truth

- Repo: <https://github.com/drstrangerujn/scellrun>
- ROADMAP: `<repo>/ROADMAP.md` — version map, AIO/Rmd reference points,
  shipped versions through v0.9.
- Profiles: `<repo>/src/scellrun/profiles/` — read these to see current
  thresholds and panels.
- Decision module: `<repo>/src/scellrun/decisions.py` — schema for the
  `00_decisions.jsonl` log.
- Self-check module: `<repo>/src/scellrun/self_check.py` — trigger
  thresholds and structured fix shapes.

## Provenance

Defaults trace to the in-house R AIO pipeline (Liu lab, Nanjing) and a
clinical team's working practice for OARSI / MSK research. Where Python
lacks a stable equivalent (e.g. decontX), the relevant R-only step is
documented as "not in scope" rather than half-implemented.
