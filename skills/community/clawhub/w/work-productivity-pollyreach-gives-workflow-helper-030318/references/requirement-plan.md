# Requirement Plan

## Live Requirement

Validated demand: Agent users show strong demand for PollyReach-style workflows on Clawhub. They need practical help fixing bugs, hardening setup and safety, improving reliability, or creating adjacent skills inspired by the same job-to-be-done. This requirement is supported by 8 separate online signals across 3 source families, so it represents broader demand rather than a single isolated request.

## Audience

AI-agent users, skill authors, maintainers, and teams who want proven popular skill patterns adapted into more reliable or adjacent workflows

## Category

work-productivity

## Requirement Score

Total: 100/100

Demand: 70/70

Local feasibility: 30/30

Evidence coverage: 8 signals across 3 source families.

Scoring rationale:

- Evidence count: 8; required minimum: 3.
- Distinct source families: 3; sources: clawhub, github, hacker-news.
- Demand score: 70/70 based on corroboration, source diversity, and professional/community signal.
- Local feasibility score: 30/30.
- Implementation is a documentation, workflow, code, or analysis skill that can run on ordinary CPU hardware.
- Clawhub-derived idea: popularity is only a seed signal; this idea is scored by the same 100-point requirement scorer and must meet the implementation threshold.

## Evidence

- clawhub-popular-skill (2026-07-05T13:28:03.853000+00:00): [Popular Clawhub skill demand: self-improving agent has 468,442 downloads](https://clawhub.ai/skills/self-improving-agent)
- clawhub-popular-skill (2026-05-18T03:40:07.591000+00:00): [Popular Clawhub skill demand: SkillScan has 179,594 downloads](https://clawhub.ai/skills/skillscan)
- clawhub-popular-skill (2026-05-11T09:38:07.825000+00:00): [Popular Clawhub skill demand: PollyReach has 100,159 downloads](https://clawhub.ai/skills/pollyreach)
- hacker-news-ask-hn (2026-07-16T13:54:59+00:00): [GitHub banned my account after my projects suddenly spiked on Reddit](https://news.ycombinator.com/item?id=48934639)
- hacker-news-ask-hn (2026-07-16T14:01:41+00:00): [Ask HN: Assistive Tech Ideas for Dementia](https://news.ycombinator.com/item?id=48934733)
- hacker-news-ask-hn (2026-07-16T08:06:28+00:00): [Thinking: Alternate Distribution for Filmmakers](https://news.ycombinator.com/item?id=48931604)
- github-issues (2026-07-17T03:00:58+00:00): [[Good First Issue] 🎎 Add new Trivia Question 103 - Beginner-Friendly Open-source Contribution](https://github.com/lingdojo/kana-dojo/issues/24852)
- github-issues (2026-07-17T02:53:31+00:00): [dev_tools/packaging/produce_package.sh should update CITATION.cff](https://github.com/quantumlib/OpenFermion/issues/1423)

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

Keywords: work-productivity, pollyreach, gives, every, phone, number, ability, things, done, bug fix

Trigger sentences:

- Help me Agent users show strong demand for PollyReach-style workflows on Clawhub. They need practical help fixing bugs, hardenin.
- I need a practical workflow for Agent users show strong demand for PollyReach-style workflows on Clawhub. They need practical help fixing bugs, hardenin.
- Use $work-productivity-pollyreach-gives-workflow-helper to handle Agent users show strong demand for PollyReach-style workflows on Clawhub. They need practical help fixing bugs, hardenin.
