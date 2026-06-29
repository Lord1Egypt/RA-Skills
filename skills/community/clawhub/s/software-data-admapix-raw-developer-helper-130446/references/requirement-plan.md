# Requirement Plan

## Live Requirement

Validated demand: Agent users show strong demand for AdMapix-style workflows on Clawhub. They need practical help fixing bugs, hardening setup and safety, improving reliability, or creating adjacent skills inspired by the same job-to-be-done. This requirement is supported by 6 separate online signals across 4 source families, so it represents broader demand rather than a single isolated request.

## Audience

AI-agent users, skill authors, maintainers, and teams who want proven popular skill patterns adapted into more reliable or adjacent workflows

## Category

software-and-data

## Requirement Score

Total: 100/100

Demand: 70/70

Local feasibility: 30/30

Evidence coverage: 6 signals across 4 source families.

Scoring rationale:

- Evidence count: 6; required minimum: 3.
- Distinct source families: 4; sources: clawhub, github, hacker-news, v2ex.
- Demand score: 70/70 based on corroboration, source diversity, and professional/community signal.
- Local feasibility score: 30/30.
- Implementation is a documentation, workflow, code, or analysis skill that can run on ordinary CPU hardware.
- Clawhub-derived idea: popularity is only a seed signal; this idea is scored by the same 100-point requirement scorer and must meet the implementation threshold.

## Evidence

- clawhub-popular-skill (2026-05-11T07:50:52.489000+00:00): [Popular Clawhub skill demand: ontology has 190,359 downloads](https://clawhub.ai/skills/ontology)
- clawhub-popular-skill (2026-06-19T07:09:19.124000+00:00): [Popular Clawhub skill demand: AdMapix has 131,316 downloads](https://clawhub.ai/skills/admapix)
- clawhub-popular-skill (2026-05-11T07:50:48.771000+00:00): [Popular Clawhub skill demand: Agent Browser has 127,492 downloads](https://clawhub.ai/skills/agent-browser-clawdbot)
- hacker-news-ask-hn (2026-06-22T05:08:11+00:00): [LM Link – This is the future I want](https://news.ycombinator.com/item?id=48625932)
- v2ex-latest (2026-06-22T11:32:53+00:00): [使用 ai 编程一年多，我遇到的问题以及解决思路](https://www.v2ex.com/t/1222066)
- github-issues (2026-06-22T13:01:39+00:00): [Feature Request: make app errors network-aware](https://github.com/Makerspace-Ashoka/smart-db/issues/27)

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

Keywords: software-and-data, admapix, raw, data, layer, creatives, apps, rankings, revenue, bug fix

Trigger sentences:

- Help me Agent users show strong demand for AdMapix-style workflows on Clawhub. They need practical help fixing bugs, hardening s.
- I need a practical workflow for Agent users show strong demand for AdMapix-style workflows on Clawhub. They need practical help fixing bugs, hardening s.
- Use $software-data-admapix-raw-developer-helper to handle Agent users show strong demand for AdMapix-style workflows on Clawhub. They need practical help fixing bugs, hardening s.
