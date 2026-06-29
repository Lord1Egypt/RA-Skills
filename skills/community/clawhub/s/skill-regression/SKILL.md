---
name: skill-regression
description: >
  Regression testing framework for AgentSkills. Analyzes a target skill, runs script-layer
  assertions and AI-layer semantic scoring, and outputs a Markdown report. Supports two
  backends: OpenAI-compatible LLM (default, works anywhere) or OpenClaw cron-based agent
  trigger (auto-detected if openclaw CLI present). Use when the user asks to "test a skill",
  "regression test xxx skill", "run skill QA", or "audit my skill against test cases".
  Requires SR_LLM_API_KEY env var or interactive setup; supports .env files.
---

# Skill Regression

- **Version**: 1.0.3
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-regression
- **Part of**: [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite — see [Stages](https://github.com/Songhonglei/build-better-skills#stages) for the lifecycle map.

## What it does

Given a target skill directory, this skill:

1. Normalizes test file naming (TEST.md is canonical; legacy Test.md/TESTS.md auto-renamed)
2. Loads or LLM-generates structured test cases
3. Runs script-layer assertions (subprocess + regex/contains/exact)
4. Runs AI-layer semantic scoring (LLM-as-judge, configurable threshold)
5. Outputs a Markdown report (with optional upload hook)

Two execution backends, auto-detected:

| Backend | When | What it tests |
|---------|------|---------------|
| `api` (default outside OpenClaw) | LLM API + system prompt | Whether SKILL.md is well-written enough for LLMs to follow correctly |
| `openclaw` (default inside OpenClaw) | Cron probe job → real agent → jsonl polling | End-to-end agent + skill integration |

## Quick start

```bash
# 1. First time: configure your LLM
python3 scripts/setup.py

# 2. Run regression on a skill
bash scripts/run_regression.sh /path/to/my-skill

# 3. Detailed mode (full input/output per case)
bash scripts/run_regression.sh /path/to/my-skill --detail

# 4. Re-run only failed cases from a previous run
bash scripts/run_regression.sh /path/to/my-skill \
  --rerun ~/.skill-regression-space/output/my-skill/20260622_001500
```

## Configuration (SR_* env vars, .env supported)

Required for `api` backend:

- `SR_LLM_API_KEY` — OpenAI-compatible API key (e.g. `sk-...`)
- `SR_LLM_BASE_URL` — LLM endpoint (default: `https://api.openai.com/v1`)
- `SR_LLM_MODEL` — Model name (default: `gpt-4o-mini`)

Additional for `openclaw` backend:

- `SR_TARGET_AGENT` — Target agent name in OpenClaw (default: `main`)

Config resolution priority (high → low):

1. CLI args (e.g. `--backend api`)
2. Process env vars (`export SR_LLM_API_KEY=...`)
3. Project-local `./.env` file (auto-added to `.gitignore`, chmod 600)
4. Global `~/.config/skill-regression/.env` (chmod 600)
5. Missing required keys → interactive onboarding (Style A) if TTY, else hint and exit 2 (Style B)

Defaults are NOT applied unless user explicitly accepts them during onboarding.

## Setup commands

```bash
python3 scripts/setup.py              # Interactive onboarding
python3 scripts/setup.py --show       # Show current config (secrets masked)
python3 scripts/setup.py --reset      # Wipe and re-onboard
```

## Options

```
Usage: bash scripts/run_regression.sh <skill-dir> [options]

  --backend <openclaw|api>    Test backend (default: auto-detect)
  --space-dir <path>          Workspace root (default: ~/.skill-regression-space)
  --threshold <N>             AI semantic score pass threshold (default: 7)
  --timeout <sec>             Per-case AI-layer timeout (default: 120)
  --cases <N>                 Auto-generated normal cases (default: 3, range 2-20)
  --error-cases <N>           Auto-generated error cases (default: 2, range 1-5)
  --rerun <dir>               Re-run only failures from a previous output dir
  --skip-agent                Script layer only (no LLM/agent layer)
  --no-ai-suggestions         Skip LLM-generated improvement suggestions
  --detail                    Detailed report (full input/output per case)
  --setup                     Run interactive onboarding
  -h, --help                  Show this help
```

## TEST.md format (placed in target skill dir)

````markdown
# TEST.md

## Test Cases

### Case 1: basic
```yaml
id: case_001
name: Basic functionality
type: normal                    # normal | error | edge
trigger: "user message to simulate"
script_cmd: "python3 {SKILL_DIR}/scripts/foo.py"
expected_output: "Success"      # keyword/regex; empty = no script assertion
expected_output_mode: contains  # contains | regex | exact
expected_agent_response: "describe expected agent response semantics"
skip_agent: false               # true = script layer only
```
````

Path placeholders in `script_cmd`:

| Placeholder | Resolves to |
|---|---|
| `{SKILL_DIR}` | absolute path of target skill |
| `{TESTRES_DIR}` | `~/.skill-regression-space/testres/<skill-name>` (long-term test resources) |
| `{WORK_DIR}` | `~/.skill-regression-space/output/<skill-name>/<timestamp>` (this run output) |

## Directory structure

```
~/.skill-regression-space/
├── testres/<skill-name>/    Test resources (fixtures, helper scripts) — long-term
└── output/<skill-name>/<timestamp>/
    ├── cases.json
    ├── results/
    │   ├── script_results.json
    │   └── agent_results.json
    └── report.md
```

## Report upload (optional hook)

Set the env var **SR_REPORT_UPLOAD_HOOK** (pointing to your upload script) to push the generated report somewhere:

```bash
# Your upload.sh receives: $1=report-path, $2=skill-name, $3=date
# Must print the resulting URL to stdout on success
SR_REPORT_UPLOAD_HOOK=~/bin/gist-upload.sh \
  bash scripts/run_regression.sh /path/to/my-skill
```

## Semantic scoring rubric

The LLM-as-judge returns 0-10:

| Score | Meaning |
|-------|---------|
| 9-10 | Fully matches expectations, accurate, well-formatted |
| 7-8 | Acceptable with minor issues |
| 5-6 | Partial match, core deficiencies |
| 3-4 | Major deviation, only some content matches |
| 0-2 | Wrong or unparseable |

⚠️ The judging LLM and the simulating LLM are typically the same family — treat scores
as directional, not absolute. Always inspect detailed mode reports for high-stakes calls.

## Internal modules

| File | Purpose |
|------|---------|
| `scripts/_lib_config.py` | Config loader (.env layers, onboarding) |
| `scripts/_lib_llm.py` | OpenAI-compatible LLM client (chat/score/infer) |
| `scripts/setup.py` | Interactive onboarding entry |
| `scripts/run_regression.sh` | Main pipeline orchestrator |
| `scripts/normalize_testfile.py` | TEST.md naming normalization |
| `scripts/analyze_skill.py` | Load TEST.md or LLM-generate cases |
| `scripts/run_script_tests.py` | Script-layer assertions |
| `scripts/run_agent_tests.py` | AI-layer (dual backend) |
| `scripts/generate_report.py` | Merge results + Markdown report |
| `scripts/merge_results.py` | --rerun result merging |
| `references/TEST_template.md` | TEST.md template reference |
| `references/report_structure.md` | Report structure reference |

## Dependencies

- **Required**: Python 3.8+, `python3`, `bash`, `pip install pyyaml`
- **Optional (for `openclaw` backend)**: `openclaw` CLI

No external Python packages beyond `pyyaml`. Network calls use stdlib `urllib`.

## Notes & limitations

- `api` backend tests "would an LLM follow this SKILL.md correctly?" — useful for skill
  documentation quality but does NOT test true agent + skill interaction.
- `openclaw` backend requires running inside an OpenClaw runtime and creates a
  namespaced cron job (`skill-regression-probe-<agent>-<uuid>`) per target agent.
- The normalize_testfile script will rename Test.md/TESTS.md → TEST.md in the target
  skill dir. Use `--dry-run` to preview.
- Auto-generated placeholder cases are marked `skip_agent=true` to avoid false-positive
  AI-layer scores; users should fill in a real TEST.md ASAP.
