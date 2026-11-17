---
name: architecture-scaffolding
description: Use when converting business logic or product intent into architecture diagrams, modules, data models, API contracts, and implementation scaffolds.
version: 0.1.0
status: preview
language: en
type: decompression
models:
  - Codex
  - Claude
---

# Architecture Scaffolding Skill

## When To Use

Use this skill when the user has a business idea, product mechanism, workflow, or system requirement and needs it decompressed into an engineering-ready structure.

Good fit:

- A product feature needs modules, entities, APIs, and implementation phases.
- A business rule needs a database model and service boundaries.
- A vague system idea needs a clear architecture before coding starts.

## Inputs

Ask for or infer:

- Business goal and target users.
- Core rules, states, and events.
- Required inputs, outputs, and integrations.
- Constraints such as budget, stack, privacy, compliance, or deployment target.
- Preferred output format: Mermaid, file tree, API spec, SQL schema, task plan, or all of them.

## Workflow

1. Restate the system goal in one sentence.
2. Extract the domain entities, state transitions, and core business rules.
3. Separate computation from presentation:
   - Computation: business logic, data state, validation, API behavior.
   - Presentation: UI layout, report shape, copy, charts, or rendered views.
4. Produce a high-level architecture diagram.
5. Define modules, responsibilities, and boundaries.
6. Define data models and API contracts.
7. Generate an implementation scaffold or repository tree when coding is expected.
8. Add validation checks and open questions.

## Output Contract

Return the result in this order:

1. `System Summary`
2. `Assumptions`
3. `Architecture Diagram`
4. `Domain Model`
5. `Module Boundaries`
6. `API Contracts`
7. `Implementation Scaffold`
8. `Validation Checklist`
9. `Open Questions`

## Codex Notes

Codex should turn the architecture into files only after inspecting the existing repository. It should follow local patterns, run targeted checks, and avoid unrelated refactors.

## Claude Notes

Claude should emphasize reasoning quality, tradeoffs, domain boundaries, and clear written architecture before implementation.

## Boundaries

- Do not invent unsupported business requirements.
- Do not mix rendering logic into core computation.
- Do not generate production code before the architecture has stable boundaries.
- Do not expose secrets, private data, or proprietary material in examples.

## Example Prompt

```text
Use the Architecture Scaffolding Skill.

Goal: Build a membership points system for a pet supplement store.
Rules: Users earn points from purchases, reviews, and referrals. Points can be spent on coupons. Membership level affects point multiplier.
Output: Mermaid architecture, data model, API contract, and implementation scaffold.
```
