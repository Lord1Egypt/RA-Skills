---
name: using-agent-skills-router
description: "Route ambiguous agent work to the right skill, command style, and effort level. Use when a task mentions skills, agents, workflows, lifecycle commands, review personas, ClawHub packaging, Codex or Claude skill adaptation, or when many skills could trigger and Codex needs a concise selection plan before acting."
---

# Using Agent Skills Router

Use this skill as a lightweight dispatcher. It decides which skill, workflow, or role should handle a request, then keeps the active path proportional to the task.

## Routing Workflow

1. Restate the user goal in one sentence.
2. Classify the request:
   - `tiny`: answer or edit directly; avoid ceremony.
   - `implementation`: choose the most specific build or domain skill.
   - `review`: choose a review skill or a reviewer persona.
   - `ship`: choose a lifecycle or release skill.
   - `unclear`: gather repo context first, then decide.
3. Select the smallest useful skill set. Prefer one primary skill and at most one support skill.
4. State the route briefly before executing: `Using <skill> because <reason>`.
5. If no skill matches, continue with normal Codex behavior and say no specialized skill was needed.

## Skill Selection Rules

- Prefer exact domain skills over broad lifecycle skills.
- Prefer repository-native tools, tests, and docs over generic checklists.
- Use a lifecycle skill only when the user wants planning, implementation, verification, review, or shipping as a process.
- Use a high-risk review skill when the task touches security controls, credentials, data deletion, public release, money, production systems, or broad permissions.
- Avoid stacking skills that repeat the same gate. One clear review path is better than several shallow ones.

## Output Shape

For a routing-only answer, return:

```text
Route: <skill-or-direct>
Reason: <one sentence>
Next action: <what Codex should do now>
```

For execution tasks, keep the routing note short and then proceed. Do not create docs or task files unless the user asks or the chosen skill requires durable artifacts.

## Anti-Patterns

- Do not turn small fixes into a full spec-plan-build-review cycle.
- Do not load long reference files just to decide whether a skill applies.
- Do not role-play multiple agents when the runtime cannot actually isolate their work.
- Do not ask the user which skill to use when local context makes the choice clear.
