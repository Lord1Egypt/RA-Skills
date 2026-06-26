# Skill Quality Checklist

> Load this when reviewing a skill or doing final checks before production.

## Structure

- [ ] SKILL.md YAML metadata includes `name` and `description`
- [ ] `description` contains trigger keywords (or `read_when` for WorkBuddy)
- [ ] Workflow steps are clear; each step tagged `[Deterministic]` or `[LLM]`
- [ ] Has a "Hard Rules" section
- [ ] Has a "Failure Handling" section
- [ ] Has an "Output Format" definition

## Principles

- [ ] **Simplicity first**: Is this the simplest approach? Have all removable steps been removed?
- [ ] **Workflow vs Agent**: Correctly chose workflow/agent? (Most should be workflows)
- [ ] **Pattern match**: Which workflow pattern was selected? What's the rationale?
- [ ] **LLM minimized**: Are all deterministic steps using scripts/deterministic logic instead of LLM?
- [ ] **Progressive disclosure**: Are references loaded on-demand or all pre-loaded? (Should be on-demand)

## Tools & Paths

- [ ] All file references use **absolute paths** or paths clearly relative to Skill directory
- [ ] Tool descriptions are unambiguous (parameter names like `user_id` not `user`)
- [ ] Return values contain only high-signal info (name, content), not low-value metadata (UUID, mime_type)

## Guardrails

- [ ] Input validation: Does it check input validity?
- [ ] Output filtering: Is there a sensitive content check?
- [ ] Failure handling: Every possible failure scenario has a response?
- [ ] Human-in-the-loop: Are there checkpoints before high-risk outputs?

## Observability

- [ ] Can you trace which materials the Skill referenced?
- [ ] Can you pinpoint which step failed when errors occur?

## Production-Ready Extensions (Optional)

For skills running in automation or serving multiple users:

- [ ] **Quality vs Latency**: Have you traded off accuracy against response time?
- [ ] **Guardrails**: Input validation, output filtering, human checkpoints before high-risk outputs
- [ ] **Evaluation**: End-to-end quality checks, component-level accuracy tests, continuous monitoring
