## Description:

支持站站、车次、余票查询，返回时刻、票价与余票等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query China train routes, train-number details, schedules, fares, and remaining ticket availability through JisuAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Train search details and the JisuAPI AppKey are sent to JisuAPI when the skill runs.

Mitigation: Use a dedicated, quota-limited JisuAPI key and run the skill only when sharing the requested train search details with JisuAPI is acceptable.

Risk: Request URLs, command history, or logs may expose the JisuAPI AppKey.

Mitigation: Avoid sharing logs that include request URLs, keep the key in the JISU_API_KEY environment variable, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/train)
- [JisuAPI train API documentation](https://www.jisuapi.com/api/train/)
- [JisuAPI website](https://www.jisuapi.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [JSON responses from command-line API queries, with text guidance for setup and usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JISU_API_KEY environment variable.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
