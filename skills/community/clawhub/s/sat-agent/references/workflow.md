# Workflow

## When to use

Use this skill inside a workspace that already contains the QLCoder project and its `qlcoder` Python package.

Two entry points are supported:
- CVE sample pure-LLM analysis from a manifest.
- Local repository pure-LLM analysis with Java/Python Web taint-profile typing.

Local mode additionally emits triaged findings for common web-app risk classes (XSS, SQLi, broken access control).

## Commands

### Manifest/CVE Mode

Build or refresh a base manifest:

```bash
python -m qlcoder.cli build-manifest --base-only --allow-manual-override --manual-base-ref master
```

Choose the default seed sample:

```bash
python -m qlcoder.cli choose-seed --manifest datasets/manifests/qlcoder_base_111.csv
```

Run one sample in pure-LLM mode:

```bash
python -m qlcoder.cli run-one-pure-llm --project-slug <slug> --manifest datasets/manifests/qlcoder_base_111.csv
```

Run a batch in pure-LLM mode:

```bash
python -m qlcoder.cli run-manifest-pure-llm --manifest datasets/manifests/qlcoder_base_111.csv --limit 5
```

### Local Web App Mode

Analyze one local repository (QLCoder built-in local pure-LLM):

```bash
python -m qlcoder.cli run-local-pure-llm --repo-path /path/to/web-app --analysis-name my-app
```

Prefer the wrapper for profile typing artifacts:

```bash
python /Users/aibot/.codex/skills/coder-pure-llm/scripts/run_pure_llm.py \
  --workspace /path/to/qlcoder-workspace \
  --repo-path /path/to/web-app \
  --app-profile auto
```

Review order:
1. `taint_findings.analysis.json` for prioritized findings.
2. `taint_profile.analysis.json` for source/sink/sanitizer detail and manual trace.

## Wrapper script

Prefer the bundled wrapper:

```bash
python /Users/aibot/.codex/skills/coder-pure-llm/scripts/run_pure_llm.py --workspace /path/to/project
```

Useful flags:

- `--project-slug <slug>`: run a specific sample
- `--manifest <path>`: use an explicit manifest
- `--build-base-manifest`: force base manifest creation before running
- `--batch-limit N`: run a limited batch instead of one sample
- `--repo-path <path>`: run local repository pure-LLM analysis
- `--analysis-name <name>`: customize local run directory name
- `--app-profile auto|java-web|python-web`: control taint source/sink/sanitizer typing profile

## Interpretation

### Manifest/CVE Mode JSON fields

- `summary`
- `source_hypotheses`
- `sink_hypotheses`
- `sanitizer_hypotheses`
- `additional_flow_steps`
- `draft_query_strategy`
- `draft_query_text`
- `limitations`

### Local Web App Taint Profile JSON fields

`taint_profile.analysis.json` contains:

- `selected_profiles`
- `summary.source_hits`
- `summary.sink_hits`
- `summary.sanitizer_hits`
- `profile_reports[].source_types[]`
- `profile_reports[].sink_types[]`
- `profile_reports[].sanitizer_types[]`
- `limitations`

### Local Web App Findings JSON fields

`taint_findings.analysis.json` contains:

- `summary.finding_count`
- `summary.high|medium|low`
- `findings[].category`
- `findings[].severity`
- `findings[].confidence`
- `findings[].evidence[]`
- `findings[].recommendations[]`
- `limitations`

Current findings detector focuses on:
- `xss`: unescaped sink patterns (for example `th:utext`) plus filter policy context.
- `sql-injection`: dynamic SQL sink markers (for example `${sql}`) with guard awareness.
- `broken-access-control`: mapped demo/test controllers without fine-grained permission annotations.

Always mention that outputs are draft candidate analysis without CodeQL compilation or execution.
