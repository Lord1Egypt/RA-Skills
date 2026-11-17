<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-mirror banner" width="100%" />
</p>

<h1 align="center">yotta-mirror · 元镜 (YuanJing)</h1>

<p align="center">YottaMeta's <b>deterministic learning-diagnostics skill</b>: turn a score / answer sheet
plus an item-to-knowledge map into a reproducible diagnosis report where every weak-point conclusion
carries its <b>item ids, sample size, rate and threshold</b>.</p>
<p align="center">Pure Python 3.8+ standard library, zero external dependencies; Windows + Linux + macOS;
student data stays on your machine — no network, no model calls, no upload.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-mirror"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-mirror" /></a>
  <a href="https://github.com/YottaMeta/yotta-mirror"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-mirror" /></a>
</p>

## What it is

yotta-mirror reads a structured score sheet (CSV / TSV / stdin) and an item-to-knowledge map, then runs a
deterministic pipeline: data gate → per-item statistics → score-weighted knowledge mastery → student
layers and borderline students → weak-point diagnosis with evidence → Markdown / JSON report.

It is a teaching-improvement aid, not a student evaluation tool. It never produces rankings, comments,
or predictions, and every conclusion can be re-computed from the archived inputs.

## Core value

- **Evidence for every conclusion** — each weak point lists its items, respondents, rate and the threshold used.
- **Deterministic** — the same data and thresholds produce the same report; only `generated_at` changes.
- **Explicit thresholds** — mastery, layer and sample-size thresholds come from a JSON config and are echoed into the report.
- **Human review by default** — low-sample statistics and borderline students are downgraded to review items instead of conclusions.
- **Privacy first** — local-only, zero network imports, `--anonymize` for shareable reports.
- **Stable JSON contract** — fixed top-level schema for automation, archiving and CI gates.

## Quick start

Windows uses `python`, Linux / macOS use `python3`.

```bash
# 1. Create input templates (score sheet + item map + thresholds)
python3 scripts/yotta_mirror.py template --output-dir ./mirror-template

# 2. Analyse one quiz and print a Markdown report
python3 scripts/yotta_mirror.py analyze --input scores.csv --items item-map.json

# 3. Emit JSON and fail CI when 3 or more weak knowledge points appear
python3 scripts/yotta_mirror.py analyze --input scores.csv --items item-map.json \
  --format json --out report.json --gate weak=3

# 4. Share a report without student identifiers
python3 scripts/yotta_mirror.py analyze --input scores.csv --items item-map.json --anonymize
```

## Commands

| Command | Description |
|---|---|
| `analyze --input <file>` | Analyse a CSV / TSV score sheet |
| `analyze --stdin` | Read the score sheet from standard input |
| `analyze --items <file>` | Item-to-knowledge map (required) |
| `analyze --config <file>` | Override mastery / layer / sample-size thresholds |
| `analyze --format md\|json` | Markdown (default) or JSON report |
| `analyze --out <file>` | Write the report to a file instead of stdout |
| `analyze --anonymize` | Replace student identifiers with reproducible codes |
| `analyze --gate weak=<n>` | Exit code 1 when the weak-point count reaches `n` |
| `template --output-dir <dir>` | Write starter score sheet, item map and thresholds |
| `config validate --pack <file>` | Validate a thresholds file |
| `--version` | Print the engine version |

Exit codes: `0` ok ｜ `1` gate triggered ｜ `2` input error ｜ `3` config / map error ｜ `4` runtime error.

## Input format

```csv
student,T1,T2,T3
S01,5,3,2
S02,5,3,
```

- First column = student identifier; the remaining columns are item ids that must match the item map.
- A cell is the score for that item; blank cells count as missing and are reported separately.
- Judgement items use `0` / `1` with `max_score = 1`.

```json
{
  "schema_version": "1.0",
  "items": [
    {"id": "T1", "max_score": 5, "knowledge": ["有理数运算"], "difficulty": "easy"},
    {"id": "T2", "max_score": 3, "knowledge": ["有理数运算", "计算"]}
  ]
}
```

See [references/data-format.md](references/data-format.md) for the full schema and the error message table.

## Report contract

Markdown sections: input summary → per-item statistics → knowledge mastery → student layers →
weak-point diagnosis → human review → disclaimer.

JSON top-level keys: `schema_version`, `tool`, `tool_version`, `generated_at`, `input`, `quality`,
`items_stats`, `knowledge`, `layers`, `diagnoses`, `review_items`, `summary`, `thresholds`, `disclaimer`.

Full field list, decision rules and exit codes: [references/report-format.md](references/report-format.md).

## Privacy

- Student data never leaves the machine: the engine imports no network library and calls no model.
- `--anonymize` replaces identifiers with `S-` + the first 8 hex digits of their SHA-256, so codes are
  reproducible within a dataset but not reversible across datasets.
- Reports carry a fixed disclaimer: for teaching improvement only — not for student evaluation,
  ranking or admission decisions.

Details and a safety checklist: [references/privacy.md](references/privacy.md).

## Installation

### Option 1 — npx (recommended)

```bash
npx -y @yottameta/yotta-mirror --agent codex     # or: --agent claude | cursor | gemini | opencode ...
npx -y @yottameta/yotta-mirror --dir <skills-dir>
```

### Option 2 — git clone

```bash
git clone https://github.com/YottaMeta/yotta-mirror.git <skills-dir>/yotta-mirror
```

### Option 3 — Download ZIP

Download ZIP from https://github.com/YottaMeta/yotta-mirror and extract it into your agent's skills directory.

### Option 4 — install.sh

```bash
bash install.sh --list                  # show agent → default directory
bash install.sh --agent codex           # install for one agent
bash install.sh --dir <skills-dir>      # install into an explicit directory
```

## Works with

- **yotta-present** — render the diagnostics report into a consistent, copyable layout;
- **yotta-memory** — store report summaries and threshold versions on request;
- **yotta-compliance** — clause-level review for materials that contain student personal information;
- **yotta-humanize** — natural-language polish for teacher-facing narratives;
- **yotta-skills** — orchestrate analyse → present → record as one workflow.

## Requirements

- Python 3.8+ (standard library only)
- UTF-8 encoded CSV / TSV input; no extra packages, no database, no service

## License

MIT. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
