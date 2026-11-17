## Description:

Queries notable historical events, births, and deaths for a given month and day using the JisuAPI Today in History service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to answer history-on-this-date questions by requesting events for a specific month and day and summarizing the returned timeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each query sends the configured JISU_API_KEY and requested month/day to JisuAPI.

Mitigation: Use a scoped JisuAPI key, follow the provider's account controls, and install only when sharing those query details with JisuAPI is acceptable.

Risk: The skill depends on the availability and terms of the external JisuAPI Today in History service.

Mitigation: Handle API errors gracefully and review JisuAPI access limits, permissions, and service terms before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/todayhistory)
- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI Today in History API](https://www.jisuapi.com/api/todayhistory/)
- [Today in History Query Endpoint](https://api.jisuapi.com/todayhistory/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; query input is a JSON object with month and day.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
