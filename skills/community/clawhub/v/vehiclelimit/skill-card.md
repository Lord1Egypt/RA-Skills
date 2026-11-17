## Description:

Queries supported-city vehicle license plate restriction rules and restricted plate-ending numbers for a requested city and date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up traffic restriction details for supported Chinese cities. It can list supported cities and query date-specific restriction times, areas, summaries, number rules, and restricted plate-ending numbers through JisuAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send the requested city and date plus JISU_API_KEY to JisuAPI.

Mitigation: Use only when the user is comfortable sharing those query details with JisuAPI, and avoid adding unrelated personal information.

Risk: Use depends on JisuAPI account terms, quota, privacy expectations, and API availability.

Mitigation: Review JisuAPI terms, quota, and privacy expectations before deployment or recurring use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/vehiclelimit)
- [JisuAPI vehicle limit documentation](https://www.jisuapi.com/api/vehiclelimit/)
- [JisuAPI provider site](https://www.jisuapi.com/)
- [JisuAPI vehicle city endpoint](https://api.jisuapi.com/vehiclelimit/city)
- [JisuAPI vehicle limit query endpoint](https://api.jisuapi.com/vehiclelimit/query)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable; sends the requested city, date, and API key to JisuAPI.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
