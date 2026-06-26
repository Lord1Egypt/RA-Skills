---
name: skill-forge
description: Detect repeated capability gaps, convert recurring user needs into candidate skills, scaffold new OpenClaw-compatible skills, and validate them before installation. Use when an agent repeatedly fails the same task, sees recurring feature requests, notices repetitive manual workflows, or wants to propose a new skill instead of solving the same problem ad hoc.
---

# skill-forge

Use this skill to turn repeated demand into a reviewed skill candidate.

Current version: `v1.4.0 "Evolve First"`.

## Core jobs

1. Detect repeated capability gaps from logs, `.learnings`, and feature requests.
2. Decide whether the pattern is stable enough to deserve its own skill.
3. Classify the opportunity as `academic`, `product`, `integration`, `script`, or `workflow`.
4. Generate a candidate skill folder with a usable `SKILL.md`, `agents/openai.yaml`, and profile-specific resources.
5. Validate and score the candidate before proposing installation.
6. Run hidden smoke evaluation and Agent profile authorization before confirmed installation.
7. Record feedback from later usage and propose reviewed updates instead of mutating installed skills directly.
8. Provide the Somnia runtime used by scheduled nightly review to find skills with bugs, weak scores, or update-worthy feedback.
9. Use redacted replay cases to check whether candidates actually cover real feedback-derived tasks.
10. Provide a product console (`scripts/skill_forge.py`) so agents can run doctor checks, demos, forge flows, evolution, feedback capture, replay, and release gates from one entry point.

## Trigger Cues

Use this skill when the user or agent mentions:

- repeated failure
- missing capability
- recurring workflow
- feature request
- make a new skill
- scaffold a skill
- validate a generated skill

## Default Workflow

1. Detect repeated capability gaps from learning files or session-derived notes.
2. Classify the strongest opportunity into a skill profile.
3. When `--prefer-evolve` is set, route the opportunity through `decide_skill_action.py` first; if it matches an installed skill, evolve that skill instead of forging a new one.
4. Scaffold a candidate skill with profile-specific resources (forge path).
5. Validate the candidate and inspect score, warnings, and references.
6. Run hidden smoke evaluation without exposing simulated cases to users.
7. Propose installation, then require Telegram approval before applying it.
8. Record future usage feedback and run an evolution pipeline when enough feedback accumulates.
9. During scheduled reviews, write summary reports and optionally propose updates without exposing hidden evaluation details.
10. Run replay evaluation before approving evolved candidates when replay cases exist.
11. Before release, run package checks and golden scaffold checks across all supported profiles.
12. Run deterministic benchmarks before release to enforce validation, hidden-eval, line-count, and runtime budgets.

## Resource Loading

Keep this `SKILL.md` focused on the operating path. Load bundled references only when the current task needs them:

- Read `references/heuristics.md` when deciding whether a repeated need deserves a skill.
- Read `references/skill-quality-rubric.md` when reviewing candidate quality or explaining a validation score.
- Read `references/milestone-architecture.md` when changing install gates, replay gates, or evolution flow.
- Read `references/forge-console.md` when using or modifying the product console.

## Execution Mode

Use medium freedom for planning and candidate design, but low freedom for install, uninstall, release checks, signed approval, replay regression, and file mutation paths.

## Commands

### Forge Console

Prefer the product console for normal use:

```bash
python3 {baseDir}/scripts/skill_forge.py doctor --json
python3 {baseDir}/scripts/skill_forge.py demo --json
python3 {baseDir}/scripts/skill_forge.py forge --output ./generated --install plan --json
python3 {baseDir}/scripts/skill_forge.py release-check --json
```

From the source repository, `make package-check` runs the same release gate plus secret scanning.

Use lower-level scripts only when a workflow needs exact control over one stage.

### Detect

Run:

```bash
python3 {baseDir}/scripts/detect_skill_opportunities.py --json
```

Add `--source` paths when a specific workspace or learnings file should be analyzed.

### Decide (evolve-or-forge routing)

After detect, ask whether the opportunity should evolve an existing installed skill or forge a new one. Use this to prevent skill sprawl when a request is really just a new trigger surface for something the user already installed.

```bash
python3 {baseDir}/scripts/skill_forge.py decide \
  --skill-name "literature-review-helper" \
  --triggers "APA format, MLA format, literature review, source metadata" \
  --template academic \
  --reason "user keeps asking for APA literature reviews" \
  --json
```

Output is one of `evolve` / `forge` / `ambiguous` plus per-candidate fitness scores. To run the full pipeline with auto-routing, pass `--prefer-evolve` to `forge`:

```bash
python3 {baseDir}/scripts/skill_forge.py forge \
  --output ./generated --install plan --prefer-evolve --json
```

Profile mismatch is a hard gate (fitness 0). The replay non-regression gate downstream catches any mis-routed evolution that would degrade the installed baseline.

### Choose

Only create a skill when the pattern is:

- recurring
- broad enough to reuse
- structured enough to document
- more stable than a one-off prompt

If the need is too narrow, keep it as a note or workflow rule instead.

### Scaffold

Run:

```bash
python3 {baseDir}/scripts/generate_skill_scaffold.py \
  --skill-name my-skill \
  --output ./generated \
  --goal "What the skill should achieve." \
  --triggers "keyword1, keyword2" \
  --template auto
```

### Validate

Run:

```bash
python3 {baseDir}/scripts/validate_skill_candidate.py ./generated/my-skill
```

### Propose Installation

Plan only (safe to run anywhere, no Telegram, no secrets):

```bash
python3 {baseDir}/scripts/propose_skill_install.py ./generated/my-skill --json
```

`--apply` is gated by a signed approval token. Direct invocation without a token is blocked. Use the full pipeline (`forge_pipeline.py --install telegram`) for the normal install path, or call `telegram_approval.py` first and pass its `approval_token` to `propose_skill_install.py --apply --approval-token <token>`. The token is HMAC-bound to the skill name, target path, install method, source path, and a hash of the source directory's contents, so any post-approval edit invalidates it. Token issuance and install apply both require the source to be an existing skill directory containing `SKILL.md`.

### Record Feedback

Run:

```bash
python3 {baseDir}/scripts/record_skill_feedback.py \
  --skill my-skill \
  --agent-name StudyAgent \
  --rating negative \
  --feedback "触发词: literature review. The skill should handle literature review planning better." \
  --json
```

### Propose Evolution

Run:

```bash
python3 {baseDir}/scripts/evolve_skill_pipeline.py \
  --skill my-skill \
  --output ./generated-updates \
  --install plan \
  --replay hidden \
  --min-replay-improvement 0 \
  --agent-name StudyAgent \
  --json
```

When an installed copy of `my-skill` exists under `--target-root`, the candidate and the installed baseline are scored against the same redacted replay cases. The pipeline blocks the install when `candidate_score - baseline_score < --min-replay-improvement` (default `0`, i.e. no regression). Pass `--min-replay-improvement -100` to disable the regression check.

### Replay Evaluation

Run:

```bash
python3 {baseDir}/scripts/replay/collect_replay_cases.py \
  --feedback-file ~/.openclaw/workspace/.learnings/skill-feedback.jsonl \
  --skill my-skill \
  --json

python3 {baseDir}/scripts/replay/run_replay_eval.py \
  --skill-dir ./generated-updates/my-skill \
  --skill my-skill \
  --json
```

### Nightly Review

Somnia is now packaged as its own skill for scheduled maintenance. These compatibility commands remain available from Skill Forge:

```bash
python3 {baseDir}/scripts/nightly_skill_review.py \
  --scope managed \
  --propose-updates \
  --replay hidden \
  --update-install plan \
  --json
```

Install a macOS daily sleep-hour schedule, defaulting to 03:00 local time:

```bash
python3 {baseDir}/scripts/schedule_nightly_review.py \
  --hour 3 \
  --minute 0 \
  --scope managed \
  --propose-updates \
  --update-install plan \
  --apply \
  --json
```

Use `--telegram-report` with `--env-file ~/.openclaw/skill-forge.env` when scheduled runs should send a summary report to Telegram. The env file should define `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

Uninstall or rollback a generated skill. Like install, `--uninstall --apply` requires a signed approval token issued by `telegram_approval.py` for the same skill, target, and method. Plan-only (no `--apply`) works without a token and just prints what would happen:

```bash
# Plan (no token, no mutation)
python3 {baseDir}/scripts/propose_skill_install.py my-skill --uninstall --json

# Apply (requires a fresh approval token bound to the same skill/target/method)
python3 {baseDir}/scripts/install/telegram_approval.py \
  --skill my-skill \
  --profile workflow \
  --validation-score 100 --validation-grade milestone \
  --evaluation-score 100 --evaluation-passed \
  --target "$HOME/.openclaw/workspace/skills/my-skill" \
  --method symlink \
  --json > approval.json

APPROVAL_TOKEN="$(python3 -c 'import json; print(json.load(open("approval.json"))["approval_token"])')"

python3 {baseDir}/scripts/propose_skill_install.py my-skill \
  --uninstall --apply \
  --approval-token "$APPROVAL_TOKEN" \
  --restore-backup \
  --json
```

## Full Pipeline

For one-shot operation:

```bash
python3 {baseDir}/scripts/forge_pipeline.py \
  --source ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md \
  --source ~/.openclaw/workspace/.learnings/ERRORS.md \
  --output ./generated \
  --eval hidden \
  --json
```

Ask through Telegram before installing:

```bash
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."

python3 {baseDir}/scripts/forge_pipeline.py \
  --source ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md \
  --source ~/.openclaw/workspace/.learnings/ERRORS.md \
  --output ./generated \
  --install telegram \
  --agent-name StudyAgent \
  --json
```

## Decision rules

- Prefer creating a skill over a new agent when the new capability is narrow.
- Prefer a new agent over a skill when the work needs a distinct role, tools, and long-term memory boundary.
- Prefer `references/` when the skill mainly teaches structure and judgment.
- Prefer `scripts/` when the same code would otherwise be rewritten repeatedly.
- Default to `--install plan`; use `--install telegram` for any mutation.
- Treat `--install ask` and `--install auto` as blocked compatibility aliases.
- Do not call `propose_skill_install.py --apply` directly; `--apply` requires a signed approval token issued by `telegram_approval.py` and bound to the skill name, target, method, source path, and source content hash. The HMAC secret is `SKILL_FORGE_APPROVAL_SECRET` if set, otherwise derived from the bot token. Tokens default to a 30-minute TTL.
- A dry-run approval token (`mode=dry-run`) cannot mutate state. The pipeline reports `install_status=dry-run-blocked` and only `--allow-dry-run-install` on the install script lets it through, in which case the audit field is `approved_by=dry-run`.
- Keep `--eval hidden` for user-facing flows so simulated checks and prompts are not exposed.
- Use `--agent-name` before installation when a specific agent will receive the skill.
- Never hard-code Telegram tokens; discover them from OpenClaw/env files or environment variables.
- Redact feedback text before storing it.
- Treat feedback-driven changes as update candidates, not direct edits to installed skills.
- Install evolved skills only after validation, hidden evaluation, authorization, and approval.
- Replay runs as a non-regression gate during evolution: baseline (currently installed) and candidate are scored against the same redacted cases, and the candidate is blocked if `score - baseline < --min-replay-improvement` (default `0`). Use `--min-replay-improvement -100` to disable. When no installed baseline exists the gate falls back to a single-skill coverage check.
- Scheduled nightly review may propose updates, but install changes still require Telegram approval.
- Nightly reports should show only health summaries, not hidden evaluation prompts or simulated checks.
- Default nightly review scope is `managed`; use `--scope all` only for explicit full inventory audits.

## Output Contract

The skill-forge output should include:

- detected opportunity name
- recommended template profile
- generated candidate path
- validation score and grade
- install status
- approval status when Telegram confirmation is used
- nightly review report path when running scheduled review
- install plan
- review warnings, if any

## Quality Gates

Before proposing installation, confirm:

- the skill name is concrete and reusable
- the description has clear trigger conditions
- the generated structure matches the intended job
- the candidate improves a real recurring workflow
- validation score is at least 70
- `grade=milestone` is preferred before sharing externally
- installation threshold is at least 85 unless the user explicitly chooses otherwise
- hidden smoke evaluation passes
- target Agent profile policy allows the generated skill profile
- Telegram approval is available before applying install or uninstall changes
- feedback-derived updates are reviewed as candidates before replacing an installed skill
- replay evaluation passes when replay cases exist
- nightly review reports are written before any update proposal is installed
- scheduled automation uses explicit launchd configuration and can be uninstalled

Read `references/skill-quality-rubric.md` when evaluating a draft.

## Resources

References:
- `references/heuristics.md`
- `references/skill-quality-rubric.md`
- `references/milestone-architecture.md`
- `references/forge-console.md`

Scripts:
- `scripts/detect_skill_opportunities.py`
- `scripts/evaluate_skill_candidate.py`
- `scripts/generate_skill_scaffold.py`
- `scripts/validate_skill_candidate.py`
- `scripts/forge_pipeline.py`
- `scripts/skill_forge.py`
- `scripts/install/propose_skill_install.py`
- `scripts/install/telegram_approval.py`
- `scripts/evolve/evolve_skill_pipeline.py`
- `scripts/evolve/propose_skill_update.py`
- `scripts/evolve/record_skill_feedback.py`
- `scripts/replay/collect_replay_cases.py`
- `scripts/replay/compare_replay_outputs.py`
- `scripts/replay/redact_replay_case.py`
- `scripts/replay/replay_report.py`
- `scripts/replay/run_replay_eval.py`
- `scripts/somnia/nightly_skill_review.py`
- `scripts/somnia/schedule_nightly_review.py`

Compatibility wrappers:
- `scripts/propose_skill_install.py`
- `scripts/telegram_approval.py`
- `scripts/evolve_skill_pipeline.py`
- `scripts/propose_skill_update.py`
- `scripts/record_skill_feedback.py`
- `scripts/nightly_skill_review.py`
- `scripts/schedule_nightly_review.py`
