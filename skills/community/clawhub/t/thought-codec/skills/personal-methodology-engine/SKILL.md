---
name: personal-methodology-engine
description: Use when building a closed-loop personal AI working system that decomposes intent into execution and compresses feedback into reusable methodology.
version: 0.1.0
status: preview
language: en
type: loop
models:
  - Codex
  - Claude
---

# Personal Methodology Engine Skill

## When To Use

Use this skill when the user wants a durable personal working system rather than a single prompt, document, or code change.

Good fit:

- Turning a personal workflow into a reusable AI operating system.
- Combining planning, execution, review, and rule updates.
- Maintaining a project-specific or user-specific skill library over time.

## Inputs

Collect:

- The user's recurring goals and work domains.
- Existing skills, rules, prompts, docs, or project conventions.
- Examples of accepted work and rejected work.
- Feedback history and correction patterns.
- Risk boundaries: privacy, safety, irreversible actions, and scope.

## Workflow

1. Define the methodology scope.
2. Map current skills into decompression, compression, or loop roles.
3. Establish the four-layer rule model:
   - L1 Presentation
   - L2 Application
   - L3 Logic
   - L4 Base Protocol
4. Define the operating loop:
   - Task ingestion
   - Decompression
   - Execution
   - Telemetry
   - Compression gate
   - Regression check
   - Merge or rollback
5. Create rule update criteria.
6. Define what requires human approval.
7. Produce a maintenance plan and versioning scheme.

## Output Contract

Return:

1. `Methodology Scope`
2. `Skill Map`
3. `Four-Layer Rule Model`
4. `Agentic Loop`
5. `Update Policy`
6. `Human Approval Points`
7. `Versioning And Maintenance Plan`

## Codex Notes

Codex can maintain the local repository form of the methodology: files, skills, catalog entries, validation scripts, and docs. It should verify changes through repository checks.

## Claude Notes

Claude can help design the conceptual system, evaluate rule quality, and produce polished methodology documentation.

## Boundaries

- Do not automatically promote every correction into a durable rule.
- Do not store private material in public skills.
- Do not update high-level logic without review.
- Do not create a system that cannot explain why a rule exists.

## Example Prompt

```text
Use the Personal Methodology Engine Skill.

Goal: Build a personal AI collaboration system for open-source skill creation.
Materials: Existing skills, review corrections, repository structure, and release checklist.
Output: Skill map, four-layer rules, agentic loop, and maintenance policy.
```
