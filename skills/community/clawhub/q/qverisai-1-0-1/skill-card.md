## Description:

Search and execute dynamic tools via QVeris API for weather, search, stocks, finance, economics, geolocation, AIGC, news, social media, health data, and related external API use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pippo1980](https://clawhub.ai/user/pippo1980)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to discover QVeris-hosted API tools by capability and execute selected tools with explicit parameters from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broker broad external API searches and executions with user-provided data.

Mitigation: Use a scoped, revocable QVERIS_API_KEY, review discovered tools before execution where possible, and avoid passing secrets or sensitive personal, health, financial, or account data as parameters.

Risk: The README includes an unpinned npx installation path.

Mitigation: Prefer pinned or verified installation methods when installing the skill.

## Reference(s):

- [QVeris](https://qveris.ai)
- [QVeris API endpoint](https://qveris.ai/api/v1)
- [ClawHub skill page](https://clawhub.ai/pippo1980/skills/qverisai-1-0-1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QVERIS_API_KEY; script output can be formatted for display or emitted as raw JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
