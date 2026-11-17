# Requirement Plan

## Live Requirement

Validated demand: Agent users show strong demand for Nano Banana Pro-style workflows on Clawhub. They need practical help fixing bugs, hardening setup and safety, improving reliability, or creating adjacent skills inspired by the same job-to-be-done. This requirement is supported by 12 separate online signals across 5 source families, so it represents broader demand rather than a single isolated request.

## Audience

AI-agent users, skill authors, maintainers, and teams who want proven popular skill patterns adapted into more reliable or adjacent workflows

## Category

work-productivity

## Requirement Score

Total: 100/100

Demand: 70/70

Local feasibility: 30/30

Evidence coverage: 12 signals across 5 source families.

Scoring rationale:

- Evidence count: 12; required minimum: 3.
- Distinct source families: 5; sources: clawhub, github, hacker-news, segmentfault, v2ex.
- Demand score: 70/70 based on corroboration, source diversity, and professional/community signal.
- Local feasibility score: 30/30.
- Implementation is a documentation, workflow, code, or analysis skill that can run on ordinary CPU hardware.
- Clawhub-derived idea: popularity is only a seed signal; this idea is scored by the same 100-point requirement scorer and must meet the implementation threshold.

## Evidence

- clawhub-popular-skill (2026-05-11T07:48:49.679000+00:00): [Popular Clawhub skill demand: Nano Pdf has 115,721 downloads](https://clawhub.ai/skills/nano-pdf)
- clawhub-popular-skill (2026-05-18T20:48:27.565000+00:00): [Popular Clawhub skill demand: Nano Banana Pro has 105,036 downloads](https://clawhub.ai/skills/nano-banana-pro)
- github-issues (2026-07-14T05:37:34+00:00): [Skill Quality Report — 2026-07-14](https://github.com/weiflycc-cmd/awesome-copilot/issues/44)
- github-issues (2026-07-14T05:19:05+00:00): [Skill Quality Report — 2026-07-14](https://github.com/brettconnor/awesome-copilot/issues/18)
- github-issues (2026-07-13T06:26:28+00:00): [Skill Quality Report — 2026-07-13](https://github.com/weiflycc-cmd/awesome-copilot/issues/43)
- github-issues (2026-07-13T05:56:43+00:00): [Skill Quality Report — 2026-07-13](https://github.com/brettconnor/awesome-copilot/issues/17)
- github-issues (2026-07-11T17:17:19+00:00): [refactor(generate_image): source image model defaults from registry metadata](https://github.com/can1357/oh-my-pi/issues/5219)
- github-issues (2026-07-12T06:09:58+00:00): [Skill Quality Report — 2026-07-12](https://github.com/weiflycc-cmd/awesome-copilot/issues/42)
- github-issues (2026-07-12T05:45:46+00:00): [Skill Quality Report — 2026-07-12](https://github.com/brettconnor/awesome-copilot/issues/16)
- v2ex-latest (2026-07-14T15:28:44+00:00): [要给单词生成助记图片的 prompt，有比 deepseek pro 智能又便宜的 api 吗？](https://www.v2ex.com/t/1227317)
- hacker-news-search (2026-07-01T05:32:08+00:00): [Looking into the Past with Nano Banana Pro](https://jacob.gold/posts/looking-into-the-past-with-nano-banana-pro/)
- segmentfault-search (2026-07-14T20:10:34.923562+00:00): [HarmonyOS 开发者社区](https://segmentfault.com/brand/harmonyos-next)

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

Keywords: work-productivity, nano-banana-pro, nano, banana, pro, generate, edit, images, gemini, bug fix

Trigger sentences:

- Help me Agent users show strong demand for Nano Banana Pro-style workflows on Clawhub. They need practical help fixing bugs, har.
- I need a practical workflow for Agent users show strong demand for Nano Banana Pro-style workflows on Clawhub. They need practical help fixing bugs, har.
- Use $work-productivity-nano-banana-workflow-helper to handle Agent users show strong demand for Nano Banana Pro-style workflows on Clawhub. They need practical help fixing bugs, har.
