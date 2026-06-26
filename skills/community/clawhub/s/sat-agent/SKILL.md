---
name: qlcoder-pure-llm
description: Run the pure-LLM variant of the QLCoder workflow for both CVE samples and local Web App repositories. Supports multi-profile taint-flow analysis with source/sink/sanitizer typing for Java Web and Python Web projects without CodeQL/database build steps.
---

# QLCoder Pure LLM

Use this skill to drive `pure-llm` mode in the local QLCoder project with two workflows:
- CVE sample analysis from manifest (patch/advisory-driven).
- Local repository taint-flow typing for Web App codebases (Java Web, Python Web).

The local workflow now also emits a triaged security finding summary (`taint_findings.analysis.*`) focused on XSS / SQLi / broken-access-control classes.

## Quick Start

1. Confirm the workspace contains [qlcoder/cli.py](/Users/aibot/script/QLCoder复现/qlcoder/cli.py).
2. Prefer the helper script:
   `python /Users/aibot/.codex/skills/coder-pure-llm/scripts/run_pure_llm.py --workspace /path/to/workspace`
3. For CVE mode, optionally pass `--project-slug <slug>` or `--batch-limit N`.
4. For local Web App mode, pass:
   `--repo-path /path/to/repo --app-profile auto`
5. Read generated artifacts under `runs/.../pure-llm/`.

## Workflow

### A. CVE Manifest Mode

1. Reuse an existing manifest under `datasets/manifests/` when possible.
2. If missing, build base manifest:
   `python -m qlcoder.cli build-manifest --base-only --allow-manual-override --manual-base-ref master`
3. Run single sample (`run-one-pure-llm`) or batch (`run-manifest-pure-llm`).
4. Summarize:
   - `summary`
   - `source_hypotheses`
   - `sink_hypotheses`
   - `sanitizer_hypotheses`
   - `draft_query_strategy`
   - `draft_query_text`

### B. Local Web App Mode (Java/Python)

1. Run:
   `python /Users/aibot/.codex/skills/coder-pure-llm/scripts/run_pure_llm.py --workspace /path/to/workspace --repo-path /path/to/repo --app-profile auto`
2. `--app-profile` values:
   - `auto`: detect by repository file distribution; mixed repositories can run both Java and Python profiles.
   - `java-web`: force Java Web source/sink/sanitizer typing.
   - `python-web`: force Python Web source/sink/sanitizer typing.
3. First review `taint_findings.analysis.json/md` for prioritized findings and severity.
4. Then use `taint_profile.analysis.json/md` for deeper source/sink/sanitizer trace evidence.
5. Treat these results as taint-flow leads for manual trace confirmation.

### Source/Sink Type Reference

See [references/taint_profiles.md](/Users/aibot/.codex/skills/coder-pure-llm/references/taint_profiles.md) for the taxonomy used by the local Web App profile report.

## Output Contract

### CVE manifest mode artifacts

- `runs/<project_slug>/pure-llm/iteration_00.prompt.md`
- `runs/<project_slug>/pure-llm/iteration_00.analysis.json`
- `runs/<project_slug>/pure-llm/iteration_00.analysis.md`
- `runs/<project_slug>/pure-llm/iteration_01.analysis.json`
- `runs/<project_slug>/pure-llm-summary.json`

### Local Web App mode artifacts

- `runs/local-<analysis_name_or_repo>/pure-llm/analysis.json`
- `runs/local-<analysis_name_or_repo>/pure-llm/analysis.md`
- `runs/local-<analysis_name_or_repo>/pure-llm/taint_profile.analysis.json`
- `runs/local-<analysis_name_or_repo>/pure-llm/taint_profile.analysis.md`
- `runs/local-<analysis_name_or_repo>/pure-llm/taint_findings.analysis.json`
- `runs/local-<analysis_name_or_repo>/pure-llm/taint_findings.analysis.md`

Treat JSON artifacts as source of truth. Use Markdown for human-readable review.

## Notes

- Do not claim CodeQL validation in this mode.
- Missing patch or advisory files are tolerated; the workflow should still proceed using whatever metadata is available.
- Taint profile output is pattern-based candidate analysis, not full dataflow proof.
- Java `${...}` sink typing is de-noised to mapper SQL context to avoid common `pom.xml`/config placeholder false positives.
- The findings summary is heuristic triage; always verify exploitability with targeted trace/tests.
- For detailed command patterns and wrapper usage, read [references/workflow.md](/Users/aibot/.codex/skills/coder-pure-llm/references/workflow.md).
