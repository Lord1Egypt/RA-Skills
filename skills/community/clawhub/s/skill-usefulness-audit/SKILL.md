---
name: skill-usefulness-audit
slug: skill-usefulness-audit
description: Review your installed agent skills to see what you actually use, what overlaps, and what may no longer be worth keeping.
version: 0.3.24
tags: ["audit","skills","ablation","openclaw"]
user-invocable: true
disable-model-invocation: true
argument-hint: --skills-root PATH --usage-file FILE
homepage: https://github.com/gongyu0918-debug/skill-usefulness-audit
metadata: {"openclaw":{"skillKey":"skill-usefulness-audit","requires":{"bins":["python"]},"homepage":"https://github.com/gongyu0918-debug/skill-usefulness-audit"}}
---
# Skill Usefulness Audit

## Manual Trigger Only

Use this skill only after a direct request to audit installed agent skills, their usage, overlap, cleanup options, or a structure-only inventory.
Do not invoke it during normal tasks or use it for ordinary repository/source-code review, general security audit, or employee/human skill assessment.

## Safety

Never delete, merge, quarantine, isolate, or disable skills automatically.
Treat `delete`, `merge-delete`, and `quarantine-review` as manual-review recommendations.
Do not delete skills based only on a structure-only report.
This tool does not automatically replay historical conversations; it generates ablation plans and reads ablation result files that the user provides.

## Audit Scope

Audit these layers in order:

1. Usage evidence, including recency and source quality.
2. Installed metadata, instructions, and functional overlap.
3. User-provided skill-on versus skill-off results for general skills.
4. Runtime and bundle burden, including over-triggering, context cost, weak progressive disclosure, redundant resources, script failures, and private-looking files.
5. Static health and risk hints.
6. Optional offline community or registry metrics.

Treat API and tool skills as protected capability skills during ablation.
Examples: Excel, DOCX, PDF, browser automation, deployment, OCR, external API wrappers, MCP/API gateway helpers.

## Workflow

1. Collect user-provided roots before host-local defaults.
2. Load only the usage, history, ablation, and community evidence that is available.
3. Inspect each `SKILL.md` and its script/reference/asset metrics.
4. Let the bundled script classify each skill as `api`, `tool`, or `general` and calculate its score. Read `{baseDir}/references/scoring-rubric.md` only when checking or explaining a score, verdict, or action.
5. Print the short usefulness report and, when requested, write Markdown evidence or an ablation plan.

## Ablation Rules

Read `{baseDir}/references/ablation-protocol.md` only when running replays, preparing normalized ablation records, or reviewing mixed or delete-boundary results. The script can generate an ablation plan without loading the protocol.
Replay only selected `general` candidates with identical prompts/artifacts and pairwise judging.
Do not fake no-tool ablation for `api` or `tool` skills; use the rubric's protected-capability branch.

## Run the Audit

Run the audit after collecting available evidence:

```bash
REPORT_LANGUAGE=en  # use zh-CN when the current user invocation is Chinese
python "{baseDir}/scripts/skill_usefulness_audit.py" audit \
  --skills-root ./skills \
  --report-language "$REPORT_LANGUAGE" \
  --markdown-out ./skill-audit-report.md
```

OpenClaw expands `{baseDir}` to the installed skill directory. Use it for bundled scripts and references.

Add evidence only when available:

- `--usage-file`: JSON, JSONL, CSV, or TSV with per-skill usage.
- `--history-file`: raw transcripts used only when direct usage is weak or missing; mentions remain `history_mentions` / `suspected_invocations`, not `calls`.
- `--ablation-file`: normalized JSON or JSONL skill-on/skill-off results.
- `--community-file`: offline JSON, JSONL, CSV, or TSV registry metrics.
- `--ablation-plan-out`: a cost estimate and focused replay plan; its case counts can be overridden with the four `--ablation-*-cases` options documented by `--help`.
- `--json-out`: machine-readable evidence only when requested or needed by another tool.

Pass `--report-language zh-CN` for a Chinese invocation and `--report-language en` for an English invocation. `auto` reads `SKILL_AUDIT_REPORT_LANGUAGE` or the process locale, then falls back to English.

Run without extra files only when you need a structure-only audit.
Usage, community, and ablation evidence become lower-confidence in that mode.
History and usage files may contain sensitive conversations, local paths, project names, and customer data.
Missing env means not configured in the current audit process, not proof that the skill is broken in every host.

## Output Contract

Use one run for both output layers; do not ask the user to choose a quick or full mode.
Standard output is a short natural-language report. Its opening paragraph states the audited skill count and the total characters plus approximate tokens of loaded entry descriptions. Lead with actual usage, not static risk or bundle health, and keep scores, internal codes, risk flags, and tables out of this layer.
When `--markdown-out` is provided, write the detailed evidence—with scores, action codes, missing evidence, burden, and risk notes—in the same run.
Match the user's language: clean Chinese for `zh-CN` and clean English for `en`, except for skill names and unavoidable paths or commands.

Copy the short report to chat verbatim, apart from making its evidence path clickable. Do not paste raw JSON or the full Markdown evidence unless the user asks. Read `{baseDir}/references/report-narration-prompt.md` only when another agent or host must deliver an already-generated report.

JSON includes `report_mode`, per-skill `score_breakdown`, `quality_penalty`, `quality_penalty_uncapped`, `quality_evidence`, `community_breakdown`, `action_advice`, and `risk_review`. It includes `ablation_plan` only when `--ablation-plan-out` is used. JSON emits both `risk_*` and `static_risk_*` with identical values, and `total_score` as an alias of `local_score`; treat `risk_*` and `local_score` as canonical.

Keep deletion advice conservative for system or host-core skills, and prefer narrowing or merging when overlapping skills still serve distinct host integrations.

## Resources

- `{baseDir}/scripts/skill_usefulness_audit.py`: compatibility wrapper for the modular audit package.
- `{baseDir}/scripts/skill_usefulness_audit_lib/`: collect metadata, score skills, scan static risk hints, and render Markdown reports plus optional JSON artifacts.
- `{baseDir}/references/report-narration-prompt.md`: concise prompt for turning the report into a user-facing conversational summary.
- `{baseDir}/references/scoring-rubric.md`: 10-point scoring rules, confidence logic, community prior, and action thresholds.
- `{baseDir}/references/ablation-protocol.md`: normalized replay method for historical conversations.
