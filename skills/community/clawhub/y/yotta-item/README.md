<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-item banner" width="100%" />
</p>

<h1 align="center">yotta-item · 元题 (YuanTi)</h1>

<p align="center">YottaMeta's <b>deterministic paper assembler and exam checker</b>: turn a blueprint
(item types, knowledge coverage, difficulty quotas, points, time limit) plus a local item bank into an
assembled paper whose selection is <b>reproducible from a seed</b>, then check an existing paper for
<b>unknown items, duplicates, section and points deviations, difficulty drift, coverage gaps and time overrun</b>.</p>
<p align="center">Pure Python 3.8+ standard library, zero dependencies; local-only — no network, no model
calls, no item text generation, no bundled textbook or exam material.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-item"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-item" /></a>
</p>

## What it is

yotta-item reads a local item bank (id, type, points, difficulty, knowledge, optional minutes and
source) and a blueprint, then produces:

- an assembled paper — section by section, honouring knowledge coverage first, then difficulty
  quotas; the same bank, blueprint and seed always yield the same selection;
- a coverage check — run against an existing paper (item ids only) to list deterministic findings
  such as missing sections, points deviations, difficulty drift, coverage gaps and time overrun.

It is a preparation aid. It never writes item content or answers, never predicts post-exam
difficulty or discrimination, and never ships textbook, real-exam or paper text.

## Core value

- **No generated item text** — every selected item exists in your bank; shortfalls are reported,
  not filled with invented questions.
- **Reproducible assembly** — fixed-seed deterministic selection over knowledge coverage and
  difficulty quotas; reruns and audits land on the same paper.
- **Evidence-carrying findings** — each finding lists item ids plus expected and actual values.
- **Local and zero-dependency** — Python 3.8+ standard library; no network, no model, no upload.
- **Honest measurement boundary** — difficulty labels are bank metadata; measured difficulty and
  discrimination stay in post-exam analytics (yotta-mirror).

## Quick start

Windows uses `python`, Linux / macOS use `python3`.

```bash
# 1. Create templates (bank + blueprint + paper)
python3 scripts/yotta_item.py template --output-dir ./item-template

# 2. Validate inputs
python3 scripts/yotta_item.py bank validate --bank bank.json
python3 scripts/yotta_item.py blueprint validate --blueprint blueprint.json --bank bank.json

# 3. Assemble a paper from the bank (seed-locked, reproducible)
python3 scripts/yotta_item.py assemble --bank bank.json --blueprint blueprint.json --seed 0

# 4. Check a paper; fail CI when any finding appears
python3 scripts/yotta_item.py check --bank bank.json --paper paper.json \
  --blueprint blueprint.json --gate findings=1
```

## Commands

| Command | Description |
|---|---|
| `assemble --bank <file> --blueprint <file>` | Assemble a paper from the bank |
| `assemble --seed <n>` | Fix the selection seed (default 0) |
| `assemble --format md\|json` | Markdown (default) or JSON output |
| `check --bank <file> --paper <file>` | Check an existing paper (blueprint optional) |
| `check --blueprint <file>` | Also compare sections, points, quotas and coverage |
| `check --gate findings=<n>` | Exit code 1 when the finding count reaches `n` |
| `bank validate` / `blueprint validate` | Validate bank and blueprint before CI |
| `template --output-dir <dir>` | Write starter bank, blueprint and paper |
| `--version` | Print the engine version |

Exit codes: `0` ok ｜ `1` gate triggered or assembly cannot satisfy the blueprint ｜
`2` input error ｜ `3` bank / blueprint / paper validation error ｜ `4` runtime error.

## Item bank

```json
{
  "schema_version": "1.0",
  "subject": "数学",
  "grade": "七年级上",
  "difficulty_levels": ["easy", "medium", "hard"],
  "items": [
    {
      "id": "SC-01",
      "type": "single_choice",
      "points": 3,
      "difficulty": "easy",
      "knowledge": ["一元一次方程的定义"],
      "minutes": 2,
      "source": "校本题库A"
    }
  ]
}
```

Full field list and error table: [references/bank-format.md](references/bank-format.md).

## Blueprint

```json
{
  "schema_version": "1.0",
  "title": "七年级上数学 第一单元测试",
  "total_points": 60,
  "time_limit_minutes": 60,
  "coverage": ["K3"],
  "sections": [
    {
      "id": "S1",
      "title": "选择题",
      "type": "single_choice",
      "count": 10,
      "points_each": 3,
      "difficulty": {"easy": 5, "medium": 3, "hard": 2},
      "knowledge": ["K1"]
    }
  ]
}
```

Field table, validation rules and how to write a blueprint:
[references/blueprint-format.md](references/blueprint-format.md).

## Finding kinds

Assembly: `insufficient_items`, `coverage_gap`, `time_over_budget`.
Check: `unknown_item`, `duplicate_item`, `total_points_mismatch`, `section_missing`,
`section_count_mismatch`, `section_type_mismatch`, `section_points_mismatch`,
`difficulty_mismatch`, `coverage_gap`, `time_over_budget`, `section_label_missing` —
definitions, JSON contract and exit codes: [references/report-format.md](references/report-format.md).

## Boundaries

- Item content and answers come from your bank; yotta-item never generates or rewrites them;
- Difficulty labels are relative bank metadata — measured difficulty and discrimination are
  post-exam analytics, not predictions;
- No student ranking, comments or admission predictions;
- No bundled textbook, curriculum or real-exam text; samples are synthetic placeholders.

Details: [references/privacy.md](references/privacy.md).

## Installation

### Option 1 — npx (recommended)

```bash
npx -y @yottameta/yotta-item --agent codex     # or: --agent claude | cursor | gemini | opencode ...
npx -y @yottameta/yotta-item --dir <skills-dir>
```

### Option 2 — git clone

```bash
git clone https://github.com/YottaMeta/yotta-item.git <skills-dir>/yotta-item
```

### Option 3 — Download ZIP

Download ZIP from https://github.com/YottaMeta/yotta-item and extract it into your agent's skills directory.

### Option 4 — install.sh

```bash
bash install.sh --list
bash install.sh --agent codex
bash install.sh --dir <skills-dir>
```

## Works with

- **yotta-lesson** — fill lesson example and practice slots with items selected by knowledge point;
- **yotta-mirror** — takes over after the exam: measured difficulty, mastery and class-level diagnostics;
- **yotta-present** — render assembly and review reports in a consistent, copyable layout;
- **yotta-memory** — store bank versions and assembly summaries on request (local by default).

## Requirements

- Python 3.8+ (standard library only)
- UTF-8 encoded JSON bank, blueprint and paper files; no extra packages, no database, no service

## License

MIT. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
