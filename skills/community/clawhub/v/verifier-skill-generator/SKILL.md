---
name: "verifier_skill_generator"
description: "Use when a project needs one or more verifier skills for web, CLI, or API runtime checks that the Verify agent can discover automatically."
---


# Verifier Skill Generator

Use this skill to create project-specific verifier skills.

## Workflow
1. Detect project areas and application types.
2. Decide whether each area needs web, CLI, or API verification.
3. Identify available automation tools and setup gaps.
4. Ask only the project-specific questions needed to finalize each verifier.
5. Generate verifier skill folders in the repo so verification can be repeated later.

## Guardrails
- Focus on functional verification, not unit tests or type checks.
- Use names discoverable by downstream verification tooling.
- Include setup, authentication, cleanup, and self-update behavior in each verifier.

## Example Requests
- Generate verifier skills for this frontend and API.
- Inspect the project and create runtime verifier skills the Verify agent can find.

## Inputs
- Project layout
- Detected stacks
- Verification tooling availability

## Outputs
- One or more verifier skill folders
- Project-specific setup guidance

## Success Criteria
- Relevant project areas were detected correctly.
- Generated verifiers match web, CLI, or API needs.
- Each verifier is discoverable and reusable.

## Non-Goals
- Unit-test-only verification setup
- Generic verifier templates with no project specifics

## Source Provenance
Derived from `src/commands/init-verifiers.ts`.
