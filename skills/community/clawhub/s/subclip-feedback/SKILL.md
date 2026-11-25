---
name: subclip-feedback
description: Tell the Subclip team when something is broken, missing or worth improving, through report_bug, request_feature and submit_feedback. Use when a tool fails in a way you cannot work around, when the user's request cannot be done with the available tools, when the user asks you to report a problem or suggest a feature, or to pass on feedback. Text only; never send screenshots or private content.
---

# Reporting to the Subclip team

Three tools send a report to the Subclip developers' feedback inbox (the same one as subclip.app/feedback), signed in as the user's account. The tool adds `[AGENT]` to the start of the title itself, so the team knows you wrote it and not the user.

| Situation | Tool |
| --- | --- |
| A tool errored, hung, returned something wrong, or the editor misbehaved | `report_bug` |
| The user needs something no tool or feature does, or one is too limited | `request_feature` |
| The user is happy or unhappy, something felt slow or confusing, a general improvement | `submit_feedback` |

These tools exist in the released app. A development build does not list them unless it was started with `SUBCLIP_ENABLE_AGENT_FEEDBACK=1`; if they are missing, just tell the user.

## When to file

- **On your own**, when you hit a real problem you cannot work around, or a task cannot be done because a tool is missing. Do it once per distinct problem.
- **When the user asks** you to report it or to suggest a feature. Set `initiatedBy: "user"`.
- Always **keep doing the user's task**. Filing a report never replaces helping: finish what is possible, use a workaround if there is one, and say plainly what could not be done.
- Tell the user in one sentence that you sent it. Do not ask for permission for a text report, but never promise a fix or a date.

## When not to file

- Mistakes you can fix yourself (wrong arguments, wrong order, a project that was not open): fix them.
- The same problem twice (the tool refuses duplicates, and so should you).
- Things the user can do themselves in settings (signing in, a missing permission): tell them.
- Not signed in: the tool says so. Tell the user what you found and that they can write to subclip.app/feedback.

## How to write a good report

Write for a developer who cannot see the user's screen or project:

- `title`: specific, under about 12 words. "export_video stays at 90% on a 4K project", not "export broken".
- Bug: `whatHappened`, the `tool`, the exact `errorMessage`, `stepsToReproduce` as the ordered tool calls, `expectedBehavior`, `severity` (`blocker` only when the user cannot get the result at all), and the `workaround` if you found one.
- Feature or tool: `problem` (what the user wanted and could not do), `proposal` (the tool or behaviour that would solve it, with inputs and outputs), the closest `relatedTools`, `kind` (`new-tool`, `new-feature`, `improvement`).
- Feedback: the `message`, `sentiment` and the `area`.
- `userPrompt`: what the user asked for, paraphrased. `agentClient`: which AI client you are.

## Privacy: text only

Reports are text. Never attach or describe screenshots, and never include file paths, media content, transcripts of private content, names, emails, links with tokens or any credentials. Describe the problem in words ("a 4K portrait clip with a HyperFrames caption layer"). The tool redacts obvious paths, emails and tokens, but do not rely on it. If someone wants to show a screenshot, they can send it through subclip.app/feedback themselves.

## Limits

Five reports per hour per session, and the same title only once. If you hit the limit, tell the user what you found instead.
