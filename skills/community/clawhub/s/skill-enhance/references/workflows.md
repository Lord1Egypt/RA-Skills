# Workflows

Use this file when the user needs a fixed operational process instead of loose guidance.

`SKILL.md` is the source of truth for the workflow.
This file exists to summarize and explain it, not to redefine it differently.

## Canonical Flow Summary

1. Identify mode
2. Check local editability if the target is a local skill
3. Define trigger boundary and output contract
4. Build or revise package artifacts
5. Run review gates
6. Report readiness

## New Skill Creation

- define purpose and audience
- define triggers and exclusions
- define output contract
- create package files
- add eval prompts
- review readiness

## Existing Skill Enhancement

- inspect the current package
- identify the weakest parts
- revise only the needed files
- review the updated package

## Local Skill Modification

- identify the local target
- confirm the path
- check access and writeability
- apply the local modification decision table from `SKILL.md`
- ask for edit confirmation
- modify only after confirmation
- report the exact local changes

## Publish-Readiness Review

- inspect naming and description
- inspect README and metadata
- inspect evals and references
- inspect trigger and output contract
- report readiness level and remaining gaps
