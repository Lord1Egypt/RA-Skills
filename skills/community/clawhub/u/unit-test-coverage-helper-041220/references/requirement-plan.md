# Requirement Plan

## Live Requirement

Validated demand: Teams need repeatable help adding useful unit tests and raising test coverage for existing codebases. This requirement is supported by 12 separate online signals across 3 source families, so it represents broader demand rather than a single isolated request.

## Audience

software maintainers, QA engineers, open-source contributors, and product teams who need confidence that changes do not break existing behavior

## Category

software-and-data

## Requirement Score

Total: 100/100

Demand: 70/70

Local feasibility: 30/30

Evidence coverage: 12 signals across 3 source families.

Scoring rationale:

- Evidence count: 12; required minimum: 3.
- Distinct source families: 3; sources: github, hacker-news, segmentfault.
- Demand score: 70/70 based on corroboration, source diversity, and professional/community signal.
- Local feasibility score: 30/30.
- Implementation is a documentation, workflow, code, or analysis skill that can run on ordinary CPU hardware.

## Evidence

- github-issues (2026-07-13T17:41:38+00:00): [Define FX settlement fee currency and signed cash-leg economics](https://github.com/sgajbi/lotus-core/issues/754)
- github-issues (2026-07-19T02:26:14+00:00): [Tenant pause/resume (scale-to-zero) + accurate cloud cost model](https://github.com/vitalharmony/harmonic-forge/issues/62)
- github-issues (2026-07-15T00:18:13+00:00): [Wait for analytics source readiness before latency measurement](https://github.com/sgajbi/lotus-core/issues/785)
- github-issues (2026-07-14T00:08:46+00:00): [Make repo-native Python validation worktree-isolated](https://github.com/sgajbi/lotus-core/issues/763)
- github-issues (2026-07-21T17:06:25+00:00): [chunker ignores chunk_token_num: soft cap routinely overshoots by one unit (and can blow past 100x)](https://github.com/infiniflow/ragflow/issues/17202)
- hacker-news-search (2026-07-10T20:25:10+00:00): [Skillgrade: "Unit tests" for your agent skills](https://github.com/mgechev/skillgrade)
- segmentfault-search (2026-07-23T04:12:58.851109+00:00): [HarmonyOS 开发者社区](https://segmentfault.com/brand/harmonyos-next)
- segmentfault-search (2026-07-23T04:12:58.851109+00:00): [javascript](https://segmentfault.com/t/javascript)
- segmentfault-search (2026-07-23T04:12:58.851109+00:00): [typescript](https://segmentfault.com/t/typescript)
- segmentfault-search (2026-07-23T04:12:58.851109+00:00): [ONES 研发管理](https://ones.cn/?utm_term=ONES%C2%A0%E7%A0%94%E5%8F%91%E7%AE%A1%E7%90%86&utm_campaign=%E9%A6%96%E9%A1%B5%E6%A0%87%E7%AD%BE&_channel_track_key=myqX1C0f&utm_source=%E6%80%9D%E5%90%A6%E8%BD%AC%20ONES)
- segmentfault-search (2026-07-23T04:12:58.852119+00:00): [Writing Great Unit Tests: Best and Worst Practices](https://segmentfault.com/a/1190000009709754)
- segmentfault-search (2026-07-23T04:12:58.852119+00:00): [Android自动化测试一 UiAutomator官方介绍](https://segmentfault.com/a/1190000045114982)

## How The Skill Meets The Requirement

Transforms the live request into a repeatable workflow that clarifies the user's context, produces a concrete deliverable, checks the result against the original need, and keeps execution feasible on ordinary CPU or family GPU hardware.

## Executable Implementation Plan

1. Restate the user's outcome, constraints, available inputs, and success criteria.
2. Inspect technical constraints, propose implementation steps, and include test or verification commands when code or data is involved.
3. Ask only for missing information that materially changes the output; otherwise make reasonable assumptions and continue.
4. Keep the implementation local-hardware friendly: prefer scripts, templates, checklists, and small-model or CPU-safe workflows over cloud-only or large-training approaches.
5. Produce the requested artifact, workflow, checklist, analysis, code change, or decision support.
6. Validate the output against the success criteria and list any remaining risks or follow-up work.

## Expected Outputs

- A tailored answer or artifact for the user's immediate situation.
- A reusable checklist or workflow when the task is repeatable.
- A verification note showing how the result was checked.

## Review Criteria

- The output directly addresses the discovered requirement.
- The user can act on the result without reading the original source post.
- Assumptions, limits, and required inputs are visible.
- The final response includes a short usage or next-step note when helpful.

## Usage Signals

Keywords: software-and-data, unit tests, test coverage, testing, regression, quality

Trigger sentences:

- Help me Teams need repeatable help adding useful unit tests and raising test coverage for existing codebases.
- I need a practical workflow for Teams need repeatable help adding useful unit tests and raising test coverage for existing codebases.
- Use $unit-test-coverage-helper to handle Teams need repeatable help adding useful unit tests and raising test coverage for existing codebases.
