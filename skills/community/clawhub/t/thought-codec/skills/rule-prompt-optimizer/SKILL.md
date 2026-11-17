---
name: rule-prompt-optimizer
description: Use when converting repeated feedback, corrections, and conversation traces into durable prompt rules or skill updates.
version: 0.1.0
status: preview
language: en
type: compression
models:
  - Claude
  - Codex
---

# Rule And Prompt Optimizer Skill

## When To Use

Use this skill when the user repeatedly corrects an AI system, adjusts outputs by hand, or wants conversation history turned into reusable instructions.

Good fit:

- Converting review feedback into system prompt rules.
- Updating a skill after repeated failures.
- Extracting style, structure, or decision rules from finished work.

## Inputs

Collect:

- Source material: conversation, review notes, diffs, logs, or final accepted output.
- Observed failure or repetition.
- Human correction.
- Desired reuse target: prompt rule, skill section, checklist, or policy.
- Scope: one project, one domain, or global rule.

## Workflow

1. Identify the repeated pattern.
2. Separate local preference from general rule.
3. Extract the smallest reusable instruction.
4. Assign the rule to one layer:
   - L1 Presentation
   - L2 Application
   - L3 Logic
   - L4 Base Protocol
5. Add evidence and counterexamples.
6. Create a draft patch instead of overwriting the main rule immediately.
7. Define regression checks before merging.

## Output Contract

Return:

```json
{
  "rule_id": "short-stable-id",
  "layer": "L1_Presentation | L2_Application | L3_Logic | L4_Base_Protocol",
  "instruction": "Reusable instruction",
  "evidence": ["What supports this rule"],
  "limits": ["Where this rule should not apply"],
  "regression_checks": ["Checks before merge"],
  "patch_target": "File or skill section to update"
}
```

## Codex Notes

Codex may update local prompt, skill, or documentation files after inspecting the repository and showing the intended patch through normal code-editing flow.

## Claude Notes

Claude should focus on rule clarity, overgeneralization risk, and whether the rule belongs in presentation, application, logic, or base protocol.

## Boundaries

- Do not treat one correction as a universal rule without evidence.
- Do not store private, sensitive, or proprietary examples.
- Do not update L3 or L4 rules without explicit review.
- Do not preserve noisy transcript text when a clean rule is enough.

## Example Prompt

```text
Use the Rule And Prompt Optimizer Skill.

Source: I repeatedly corrected the assistant to avoid literary metaphors and use professional technical prose.
Reuse target: Update the writing skill style rules.
Output: A draft rule patch with evidence and regression checks.
```
