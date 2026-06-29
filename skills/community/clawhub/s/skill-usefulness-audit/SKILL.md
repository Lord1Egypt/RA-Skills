---
name: skill-usefulness-audit
slug: skill-usefulness-audit
description: Audit or inventory installed agent-skill packages for cleanup using usage, overlap, burden, risk, and optional ablation/community evidence. Trigger only on explicit requests to review installed agent skills, analyze installed skill usage, or run a structure-only skill inventory; not for ordinary repository code review, general security audit, or human skills.
version: 0.3.7
tags: ["audit","skills","ablation","openclaw"]
user-invocable: true
disable-model-invocation: true
argument-hint: --skills-root PATH --usage-file FILE
homepage: https://github.com/gongyu0918-debug/skill-usefulness-audit
metadata: {"openclaw":{"skillKey":"skill-usefulness-audit","requires":{"bins":["python"]},"homepage":"https://github.com/gongyu0918-debug/skill-usefulness-audit"}}
---
# Skill Usefulness Audit

## ClawHub / OpenClaw Edition

This ClawHub bundle is packaged for OpenClaw. Install it from an OpenClaw workspace with:

```bash
openclaw skills install skill-usefulness-audit
```

OpenClaw picks up installed workspace skills in the next session. For other agent hosts, use the GitHub repository instead: https://github.com/gongyu0918-debug/skill-usefulness-audit

本 ClawHub 包是 OpenClaw 专用发布包。其他 agent 版本请访问 GitHub 仓库：https://github.com/gongyu0918-debug/skill-usefulness-audit


## Overview

Use this skill to judge whether installed agent skills still deserve to stay installed.
It turns vague "this feels useless" opinions into a repeatable audit based on usage evidence, overlap, outcome impact, quality burden, confidence, community prior, and static risk hints.

## Manual Trigger Only

Run this skill only after a direct user request.
Do not invoke it implicitly during normal task execution.
Do not use it for ordinary repository/source-code review, general security audit, employee skill assessment, or normal task execution.
Valid direct requests include installed agent skill cleanup, installed skill usage analysis, duplicate/overlap checks, and structure-only inventories of an agent skill library.

## Safety

Never delete or quarantine skills automatically.
Treat all `delete`, `merge-delete`, and `quarantine-review` results as manual-review recommendations.
Do not delete skills based only on a structure-only report.
This tool does not automatically replay historical conversations; it generates ablation plans and reads ablation result files that the user provides.

## Borrowed Idea Gate

When borrowing ideas from another skill, change one idea at a time.
Record the source idea, expected benefit, baseline command, ablation command, and rollback condition.
Keep the change only when the same input fixture improves or clarifies the target behavior without making unrelated skills stricter.

## Audit Scope

Audit these layers in order:

1. Usage evidence with recency and source quality.
2. Installed skill metadata and instructions.
3. Functional overlap across skills.
4. Ablation impact from user-provided skill-on versus skill-off results for non-API and non-tool skills.
5. Quality burden from over-triggering, context-heavy resources, weak progressive disclosure, redundant references/assets, weak scripts, or private-looking bundled files.
6. Static health and risk signals.
7. Optional offline community or registry metrics.

Treat API and tool skills as protected capability skills during ablation.
Examples: Excel, DOCX, PDF, browser automation, deployment, OCR, external API wrappers, MCP/API gateway helpers.

## Workflow

1. Collect installed skills from user-provided roots first, then host-local defaults.
2. Load usage, history, ablation, and community evidence when provided.
3. Read installed `SKILL.md` files plus script/reference/asset metrics.
4. Classify skills as `api`, `tool`, or `general`; protect `api` and `tool` skills from fake no-tool ablation.
5. Score usage, overlap, impact, quality burden, confidence, community prior, and static risk.
6. Render a Markdown report with conservative human-review actions.
7. Write a cost-efficient ablation plan only when `--ablation-plan-out` is provided.

## Ablation Rules

Read `references/ablation-protocol.md` before running ablation.

This tool does not automatically replay historical conversations.
It creates an ablation plan and reads normalized ablation result files provided by the user.

Generate an ablation plan with `--ablation-plan-out`, then replay only selected `general` skill candidates with identical prompts/artifacts and pairwise skill-on versus skill-off judging.

Do not ablate `api` or `tool` skills through fake no-tool simulations.
Use the protected-capability branch in the rubric for those skills.

## Commands

Run the audit script after collecting evidence:

```bash
python scripts/skill_usefulness_audit.py audit \
  --skills-root ./skills \
  --usage-file ./usage.json \
  --history-file ./history.jsonl \
  --ablation-file ./ablation.json \
  --community-file ./community.json \
  --report-language auto \
  --markdown-out ./skill-audit-report.md \
  --ablation-plan-out ./skill-ablation-plan.json
```

When the host exposes the skill directory, prefer an absolute script path.

Input contracts:

- `--usage-file`: JSON, JSONL, CSV, or TSV with per-skill usage evidence.
- `--history-file`: raw transcript export used only when direct usage counts are weak or missing. Mentions become `history_mentions` / `suspected_invocations`, not direct `calls`.
- `--ablation-file`: normalized JSON or JSONL with skill-on versus skill-off case results.
- `--community-file`: optional offline JSON, JSONL, CSV, or TSV registry metrics.
- `--report-language`: Markdown display language. Pass `zh-CN` when the user invoked the skill in Chinese, `en` for English, and `auto` or omit it when the language is unclear. Unsupported values fall back to English.
- `--json-out`: optional raw machine-readable report. Use it only when the user asks for JSON/raw data, another tool will consume the evidence, or you need a private local artifact for verification. Do not paste raw JSON into chat unless requested.
- `--ablation-plan-out`: optional JSON plan that estimates model cost and narrows ablation to high-value candidates.
- `--ablation-baseline-cases`, `--ablation-initial-cases`, `--ablation-expand-cases`, `--ablation-max-cases`: optional case-count overrides for the ablation plan.

Run without extra files only when you need a structure-only audit.
Usage, community, and ablation evidence become lower-confidence in that mode.
Do not delete skills based only on a structure-only report.
History and usage files may contain sensitive conversations, local paths, project names, and customer data.
Missing env means not configured in the current audit process, not proof that the skill is broken in every host.

## Output Contract

Return a front-of-report Decision Summary first, then the full score table, recommended actions, delete/merge candidates when present, missing evidence, quality burden, and risk review when relevant.

For Markdown reports, match the user's invocation language when it is supported. Keep skill names, file paths, CLI flags, env vars, action codes, risk flags, and JSON field names in English. If the user language is unsupported or unclear, use English.

Use `references/report-narration-prompt.md` to turn the report into a short conversational follow-up. The chat response should summarize decisions in plain language and mention the Markdown path; it should not expose the raw JSON file unless the user explicitly asked for it.

JSON includes `report_mode`, per-skill `score_breakdown`, `quality_penalty`, `quality_penalty_uncapped`, `quality_evidence`, `community_breakdown`, `action_advice`, and `risk_review`. It includes `ablation_plan` only when `--ablation-plan-out` is used.

Keep deletion advice conservative for system or host-core skills.
Recommend narrowing or merging before deletion when two high-overlap skills still serve distinct host integrations.
Treat `delete`, `merge-delete`, and `quarantine-review` as manual-review recommendations only; never remove or isolate a skill automatically from this report.

## Resources

- `scripts/skill_usefulness_audit.py`: compatibility wrapper for the modular audit package.
- `scripts/skill_usefulness_audit_lib/`: collect metadata, score skills, scan static risk hints, and render Markdown reports plus optional JSON artifacts.
- `references/report-narration-prompt.md`: concise prompt for turning the report into a user-facing conversational summary.
- `references/scoring-rubric.md`: 10-point scoring rules, confidence logic, community prior, and action thresholds.
- `references/ablation-protocol.md`: normalized replay method for historical conversation tests.
