## Description:

天气 helps agents answer current-weather and forecast requests without a separate API key, with Chinese-language interaction support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation workflow builders use this skill to request current weather, short-range forecasts, and weather-related status answers in Chinese-language agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, exec, and write authority that is wider than expected for a weather helper.

Mitigation: Install only after review, run it with the minimum permissions available, and approve command execution or file changes only when clearly necessary for a user-directed weather task.

Risk: The artifact contains generic automation guidance that does not fit the stated weather-query purpose.

Mitigation: Use the skill only for explicit weather queries and treat unrelated automation instructions as out of scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/weather-toolkit)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include weather query results, configuration snippets, and operational guidance depending on the user's request.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
