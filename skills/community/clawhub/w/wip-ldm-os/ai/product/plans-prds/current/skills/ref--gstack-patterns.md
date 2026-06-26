# gstack Skill Patterns Summary

**Source:** github.com/garrytan/gstack (Garry Tan)
**Retrieved:** 2026-03-25

## Overview

28 specialized skills organized into a sprint workflow: Think, Plan, Build, Review, Test, Ship, Reflect. Each skill feeds into the next. Artifacts persist.

## Architecture

- **Template system**: .tmpl files with {{PLACEHOLDERS}} resolved by `scripts/gen-skill-docs.ts`
- **Preamble**: every skill starts with bash that gathers state (update check, session tracking, config reads, git context, repo mode detection, telemetry)
- **Auto-generated**: `<!-- AUTO-GENERATED from SKILL.md.tmpl -- do not edit directly -->`
- **Two hosts**: Claude Code and Codex. Different install paths, same skills.

## Template Variables

- `{{PREAMBLE}}` ... bash initialization (update check, session tracking, config, git context)
- `{{BASE_BRANCH_DETECT}}` ... detects main/master for diff analysis
- `{{BENEFITS_FROM}}` ... lists dependent skills
- `{{DESIGN_REVIEW_LITE}}` ... conditional design review
- `{{TEST_COVERAGE_AUDIT_REVIEW}}` ... test coverage diagrams
- `{{ADVERSARIAL_STEP}}` ... dual-voice review (Claude + Codex)
- `{{COMMAND_DESCRIPTIONS}}` ... tool reference tables

## Structural Pattern (common to all skills)

1. YAML frontmatter (name, preamble-tier, version, description, allowed-tools, optional hooks)
2. Preamble section (identical across all, generated from template)
3. AskUserQuestion format guide (consistent UX)
4. Completeness Principle section
5. Repo Ownership Mode section
6. Skill-specific methodology and steps
7. Important Rules section

## Key Insight

No product pitch in any SKILL.md. Every skill is pure behavioral instruction. The AI is told WHAT TO DO, not what the product is.

Example opening (plan-ceo-review):
"You are not here to rubber-stamp this plan. You are here to make it extraordinary."

Not: "gstack is a software factory that helps you ship code faster."

## Skills List (28 total)

Planning: office-hours, plan-ceo-review, plan-design-review, plan-eng-review
Building: review, ship, investigate
QA: qa, qa-only, design-review, benchmark
Deployment: land-and-deploy, setup-deploy
Design: design-consultation
Post-Ship: document-release, retro
Multi-Model: codex, autoplan
Safety: careful, freeze, guard, unfreeze
Utility: browse, setup-browser-cookies, cso, gstack-upgrade
