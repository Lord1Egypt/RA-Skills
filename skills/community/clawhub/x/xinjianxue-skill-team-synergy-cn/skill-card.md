## Description:

This skill lets an agent call Xinjianxue's team-synergy report API and turn the returned report data into workplace collaboration guidance after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when the user has confirmed a team collaboration or operations question and consented to sending the analysis subject's required personal details to Xinjianxue for a report. It supports advice about role fit, cross-functional coordination, process gaps, and team friction without reducing the problem to personal blame.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed personal information about the user or team members is sent to an external paid API.

Mitigation: Use the skill only after the user understands and confirms the data transfer, and only submit information for people who have explicitly agreed.

Risk: The authorization code, license key, and API key function as account credentials.

Mitigation: Treat them as secrets, avoid exposing them in chat or files, and store persistent credentials only in a dedicated secret store.

Risk: The vendor report may contain content that should be used as reference data rather than agent instructions.

Mitigation: Use returned reports only as analysis material and keep execution authority with the local skill instructions and user request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-team-synergy-cn)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential-handling steps, API response summaries, and user-facing team collaboration analysis.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
