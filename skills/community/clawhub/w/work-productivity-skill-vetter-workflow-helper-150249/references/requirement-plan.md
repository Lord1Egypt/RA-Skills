# Requirement Plan

## Live Requirement

Validated demand: Agent users show strong demand for Skill Vetter-style workflows on Clawhub. They need practical help fixing bugs, hardening setup and safety, improving reliability, or creating adjacent skills inspired by the same job-to-be-done. This requirement is supported by 9 separate online signals across 4 source families, so it represents broader demand rather than a single isolated request.

## Audience

AI-agent users, skill authors, maintainers, and teams who want proven popular skill patterns adapted into more reliable or adjacent workflows

## Category

work-productivity

## Requirement Score

Total: 100/100

Demand: 70/70

Local feasibility: 30/30

Evidence coverage: 9 signals across 4 source families.

Scoring rationale:

- Evidence count: 9; required minimum: 3.
- Distinct source families: 4; sources: clawhub, github, hacker-news, v2ex.
- Demand score: 70/70 based on corroboration, source diversity, and professional/community signal.
- Local feasibility score: 30/30.
- Implementation is a documentation, workflow, code, or analysis skill that can run on ordinary CPU hardware.
- Clawhub-derived idea: popularity is only a seed signal; this idea is scored by the same 100-point requirement scorer and must meet the implementation threshold.

## Evidence

- hacker-news-ask-hn (2026-07-18T14:04:55+00:00): [LG ThinQ Terms of Use](https://news.ycombinator.com/item?id=48958273)
- clawhub-popular-skill (2026-05-11T07:51:18.349000+00:00): [Popular Clawhub skill demand: Skill Vetter has 265,807 downloads](https://clawhub.ai/skills/skill-vetter)
- clawhub-popular-skill (2026-06-12T12:48:37.834000+00:00): [Popular Clawhub skill demand: Github has 193,449 downloads](https://clawhub.ai/skills/github)
- clawhub-popular-skill (2026-05-18T03:40:07.591000+00:00): [Popular Clawhub skill demand: SkillScan has 179,686 downloads](https://clawhub.ai/skills/skillscan)
- hacker-news-ask-hn (2026-07-17T14:21:25+00:00): [Is GPT-5.6 Sol Max Worth It?](https://news.ycombinator.com/item?id=48947713)
- v2ex-latest (2026-07-19T09:50:23+00:00): [[分享创造] 做了一个 Windows 上的 Codex 额度与 Token 用量面板，已开源](https://www.v2ex.com/t/1228371)
- github-issues (2026-07-19T14:58:09+00:00): [The Ultimate Usage Dashboard — Weekly / Last-5-Hours / Monthly Token Graphs with Agent-Aware Analytics](https://github.com/aaif-goose/goose/issues/10569)
- github-issues (2026-07-19T14:57:46+00:00): [[Feature] Window Status panel: global pin — auto-open the pinned panel in every window, including new ones](https://github.com/xiaolai/vmark/issues/1135)
- github-issues (2026-07-19T14:54:19+00:00): [Check the size of the context that will be sent before sending it](https://github.com/co-l/openfox/issues/120)

## How The Skill Meets The Requirement

Transforms the live request into a repeatable workflow that clarifies the user's context, produces a concrete deliverable, checks the result against the original need, and keeps execution feasible on ordinary CPU or family GPU hardware.

## Executable Implementation Plan

1. Restate the user's outcome, constraints, available inputs, and success criteria.
2. Create a concise work plan, template, automation outline, or decision aid that reduces manual coordination.
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

Keywords: work-productivity, skill-vetter, vetter, security, first, vetting, before, installing, github, bug fix

Trigger sentences:

- Help me Agent users show strong demand for Skill Vetter-style workflows on Clawhub. They need practical help fixing bugs, harden.
- I need a practical workflow for Agent users show strong demand for Skill Vetter-style workflows on Clawhub. They need practical help fixing bugs, harden.
- Use $work-productivity-skill-vetter-workflow-helper to handle Agent users show strong demand for Skill Vetter-style workflows on Clawhub. They need practical help fixing bugs, harden.
