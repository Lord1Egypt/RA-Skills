---
name: skill-foundry
description: Discover real user demand from public online sources and turn validated opportunities into reviewed, publishable Skill packages. Use when a team wants to scan recent market signals, score demand, remove duplicate ideas, generate implementation-ready skill folders, publish to ClawHub or GitHub, and produce a catalog that explains why each skill should exist.
---

# SkillFoundry

SkillFoundry is a demand-driven Skill factory. It watches public user signals, finds repeatable jobs-to-be-done, proves that demand with evidence, and turns the strongest opportunities into documented, publishable Skill packages.

## What It Does

Use `scripts/run_skill_demand_agent.py` to run the full pipeline:

1. Search live public sources for recent user requirements.
2. Search ClawHub for popular skills above the configured download threshold and seed ideas from bug-fix, reliability, setup, safety, and adjacent-workflow opportunities.
3. Extract and rank requirement-like posts, questions, issues, and popular-skill idea seeds.
4. Corroborate each requirement with at least three separate source signals.
5. Score every idea on demand strength and local feasibility.
6. Remove repeated or same-function ideas; similar ideas only leave the strongest representative.
7. Implement only unique requirements scoring at least 90/100; ClawHub popularity never bypasses this score gate.
8. If no unique requirement reaches 90, broaden online search and try other source queries.
9. Convert accepted requirements into executable skill plans.
10. Run a final plan dedupe so same-name or same-function skills only leave one generated package.
11. Implement skill folders in parallel, capped at 10 workers.
12. Review generated skills against their plans.
13. Optionally publish reviewed skills to configured ClawHub and GitHub targets.
14. Write `SKILLS_CATALOG.md` with each skill's requirement, fit, score, evidence, keywords, and trigger sentences.

Skill names must be easy to search and easy to understand. Use short functional noun phrases like `unit-test-coverage-helper`, `openapi-docs-generator`, or `local-llm-setup-advisor`. Avoid vague action prefixes such as `assist`, `solve`, `create`, `operate`, or `streamline` unless the word is part of the actual user-facing function.

## Quick Start

Run from the repository root with Python:

```bash
python scripts/run_skill_demand_agent.py --max-ideas 10 --max-workers 10
```

Use `--max-ideas 0` to process every discovered idea. The worker cap still remains 10.
Use `--score-threshold 90`, `--min-evidence 3`, and `--max-search-rounds 3` to control the default acceptance gate.
ClawHub popular-skill discovery is enabled by default for the normal theme profile. Use `--clawhub-min-downloads 100000`, `--clawhub-popular-limit 100`, or `--no-clawhub-popular` to tune or disable that idea source.
Use `--theme-profile office` to focus discovery and scoring on Microsoft Word, Excel, PowerPoint, and cross-Office automation or file-format technical issues while keeping the same implementation and review pipeline.

## Optional Publishing

Read `references/publishing_targets.md` before changing publish behavior.

ClawHub publishing targets [https://clawhub.ai/dashboard](https://clawhub.ai/dashboard). It is possible when the local `clawhub` CLI is installed and logged in:

```bash
python scripts/run_skill_demand_agent.py --publish-clawhub
```

GitHub publishing targets a specific repository under the user's repositories, not the profile page itself. Configure a repository from [https://github.com/Kyro-Ma?tab=repositories](https://github.com/Kyro-Ma?tab=repositories), and provide `GITHUB_TOKEN` or `GH_TOKEN` with contents write permission:

```bash
python scripts/run_skill_demand_agent.py --publish-github-repo Kyro-Ma/<repo-name>
```

Use both targets together:

```bash
python scripts/run_skill_demand_agent.py --publish-clawhub --publish-github-repo Kyro-Ma/<repo-name>
```

Publishing writes `runs/<run-id>/publish_manifest.json` and `runs/<run-id>/publish_results.json` with success, failure, or skipped status for each target.

## Outputs

The runner writes:

- `generated_skills/<run-id>/`: generated skill folders.
- `runs/<run-id>/`: raw discovered requirements, plans, reviews, and run metadata.
- `runs/<run-id>/SCORING_REPORT.md`: requirement marks, source evidence, and accept/reject decisions.
- `runs/<run-id>/publish_manifest.json`: publishing targets and reviewed skill paths.
- `runs/<run-id>/publish_results.json`: publishing results when upload targets are enabled.
- `SKILLS_CATALOG.md`: latest human-readable catalog for the generated run.

Each generated skill folder includes bilingual documentation:

- `SKILL.md`: English skill instructions.
- `SKILL.zh-CN.md`: Chinese skill instructions.
- `README.md`: English user-facing summary and usage guide.
- `README.zh-CN.md`: Chinese user-facing summary and usage guide.

## Discovery Sources

Read `references/discovery_sources.md` before changing the source list, scoring rules, or extraction behavior.

## Review Standard

Treat a generated skill as complete only when it has:

- Valid `SKILL.md` frontmatter with `name` and `description`.
- English and Chinese versions of both `SKILL.md` and `README.md`.
- A requirement summary tied to at least three corroborating live source signals.
- A requirement score of at least 90/100 before implementation.
- No same-name or same-function duplicate skill; keep only the strongest representative by score, evidence count, and source diversity.
- A clear note that the implementation is feasible on ordinary CPU or family GPU hardware.
- A readable, searchable skill name that describes the function directly.
- A clear workflow, validation checklist, trigger examples, and keywords.
- `references/requirement-plan.md` with the original need, implementation plan, and review criteria.
- `agents/openai.yaml` with a default prompt that mentions the skill name.
