## Description:

A Chinese-language SBTI cyber personality-test skill that guides a user or AI agent through 30 questions and returns a formatted personality report across 27 outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choksta](https://clawhub.ai/user/choksta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run a Chinese SBTI personality test for themselves or an AI agent, including scoring, rarity lookup, radar-style dimension summaries, and a formatted result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese personality-test triggers may invoke this specific workflow for generic requests.

Mitigation: Confirm the user wants the haojiyou SBTI experience before running the full 30-question flow.

Risk: The result output includes branded text and asks users to share screenshots.

Mitigation: Treat sharing as optional and avoid including private or sensitive content in shared screenshots.

Risk: Non-Chinese users may not be well served by the default language and cultural framing.

Mitigation: Use with Chinese-speaking users or translate prompts and results when serving non-Chinese users.

## Reference(s):

- [SBTI personality database](references/personalities.md)
- [SBTI question bank](references/questions.md)
- [Original SBTI site](https://sbti.unun.dev/)
- [Original SBTI creator Bilibili profile](https://space.bilibili.com/417038183)
- [SBTI reference video](https://www.bilibili.com/video/BV1LpDHByET6/)
- [nexu-io SBTI skill repository](https://github.com/nexu-io/sbti-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style conversational prompts and final report with ASCII charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive 30-question flow with a special DRUNK result path; no shell commands, code execution, or data access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
