<p align="center"><b>Language</b>: English · <a href="./README.zh-CN.md">中文</a></p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-lesson banner" width="100%" />
</p>

<h1 align="center">yotta-lesson · 元案 (YuanAn)</h1>

<p align="center">YottaMeta's <b>deterministic lesson-plan skeleton and coverage checker</b>: turn a curriculum
map into a lesson skeleton whose stage times add up exactly and whose objectives each carry a
<b>curriculum-standard source</b>, then check an existing lesson plan for <b>missing knowledge points,
missing stages, missing citations and time mismatches</b>.</p>
<p align="center">Pure Python 3.8+ standard library, zero dependencies; local-only — no network, no model
calls, no textbook or exam text bundled.</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-lesson"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-lesson" /></a>
</p>

## What it is

yotta-lesson reads a curriculum map (lesson id, knowledge points, key points, difficulties,
misconceptions, standard reference) plus an optional structure config, then produces:

- a lesson-plan skeleton — objectives with sources, key/difficult points, misconception reminders,
  five stages with minute-level time allocation, board-work and evaluation checklist;
- a coverage check — run against an existing lesson text to list structural gaps with reasons.

It is a preparation aid. It does not write objectives on the teacher's behalf, does not generate
exercise content, and does not ship any textbook or exam material.

## Core value

- **Exact time allocation** — largest-remainder allocation, so stage minutes always sum to
  `periods × minutes_per_period`.
- **Traceable objectives** — every objective carries the `standard` reference from the map.
- **Deterministic checks** — the same lesson text, map and config produce the same gap list.
- **Local and zero-dependency** — Python 3.8+ standard library; no network, no model, no upload.
- **Metadata only** — maps hold structural metadata, never textbook or question text.

## Quick start

Windows uses `python`, Linux / macOS use `python3`.

```bash
# 1. Create templates (curriculum map + structure config)
python3 scripts/yotta_lesson.py template --output-dir ./lesson-template

# 2. Build a lesson skeleton
python3 scripts/yotta_lesson.py plan --map lesson-map.json --lesson L1

# 3. Two-period variant as JSON
python3 scripts/yotta_lesson.py plan --map lesson-map.json --lesson L1 --periods 2 --format json

# 4. Check an existing lesson plan; fail CI when any gap appears
python3 scripts/yotta_lesson.py check --plan plan.md --map lesson-map.json --lesson L1 --gate findings=1
```

## Commands

| Command | Description |
|---|---|
| `plan --map <file> --lesson <id>` | Build a lesson-plan skeleton |
| `plan --periods <n>` | Override the period count from the map |
| `plan --format md\|json` | Markdown (default) or JSON output |
| `check --plan <file>` | Check an existing lesson text for structural gaps |
| `check --stdin` | Read the lesson text from standard input |
| `check --gate findings=<n>` | Exit code 1 when the gap count reaches `n` |
| `map list / show / validate` | Inspect or validate the curriculum map |
| `template --output-dir <dir>` | Write starter map and structure config |
| `--version` | Print the engine version |

Exit codes: `0` ok ｜ `1` gate triggered ｜ `2` input error ｜ `3` map / config error ｜ `4` runtime error.

## Curriculum map

```json
{
  "schema_version": "1.0",
  "subject": "数学",
  "grade": "七年级上",
  "lessons": [
    {
      "id": "L1",
      "title": "认识一元一次方程",
      "periods": 1,
      "knowledge": ["一元一次方程的定义", "方程的解"],
      "key_points": ["一元一次方程的定义"],
      "difficulties": ["由实际问题抽象出方程"],
      "misconceptions": ["把含未知数的式子都当方程"],
      "standard": "义务教育数学课程标准（2022 年版）· 方程与不等式"
    }
  ]
}
```

Full field list and error table: [references/map-format.md](references/map-format.md).

## Gap kinds

`knowledge_missing`, `stage_missing`, `source_missing`, `time_missing`, `minutes_mismatch` —
definitions, report contract and exit codes: [references/plan-format.md](references/plan-format.md).

## Copyright and boundaries

- Maps store structural metadata only; no textbook, curriculum or exam text is bundled;
- `standard` is a citation label for traceability, not an interpretation of the curriculum;
- Output is a preparation aid — the teacher owns the final lesson design.

Details: [references/copyright.md](references/copyright.md).

## Installation

### Option 1 — npx (recommended)

```bash
npx -y @yottameta/yotta-lesson --agent codex     # or: --agent claude | cursor | gemini | opencode ...
npx -y @yottameta/yotta-lesson --dir <skills-dir>
```

### Option 2 — git clone

```bash
git clone https://github.com/YottaMeta/yotta-lesson.git <skills-dir>/yotta-lesson
```

### Option 3 — Download ZIP

Download ZIP from https://github.com/YottaMeta/yotta-lesson and extract it into your agent's skills directory.

### Option 4 — install.sh

```bash
bash install.sh --list
bash install.sh --agent codex
bash install.sh --dir <skills-dir>
```

## Works with

- **yotta-mirror** — feed learning diagnostics back into the next lesson's focus;
- **yotta-item** — assemble papers from a local item bank and run deterministic paper-structure checks (no item-text generation);
- **yotta-present** — render the skeleton in a consistent, copyable layout;
- **yotta-humanize** — natural-language polish for teacher-facing narratives;
- **yotta-memory** — store map versions and skeleton summaries on request.

## Requirements

- Python 3.8+ (standard library only)
- UTF-8 encoded JSON map and UTF-8 lesson text; no extra packages, no database, no service

## License

MIT. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
