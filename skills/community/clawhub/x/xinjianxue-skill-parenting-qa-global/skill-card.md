## Description:

XinJianXue Parent-Child Relationship Advisor helps an agent collect consented personal inputs, call the XinJianXue paid API, and provide parent-child communication guidance from both parent and child perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to request a consented parent-child relationship analysis, provide required birth, gender, and location details, and receive communication guidance based on a XinJianXue report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends birth, gender, and location details to www.xinjianxue.com and uses a paid token-based service.

Mitigation: Confirm user consent before use, collect only required details, and make token consumption clear before calling the API.

Risk: The onboarding flow handles a one-time authorization code and long-lived license and API credentials.

Mitigation: Use the authorization code only for account binding and store resulting credentials only in a trusted credential manager or user-approved environment.

Risk: The advisor provides relationship and personality-oriented guidance that could be mistaken for clinical advice.

Mitigation: Present the output as guidance, preserve the documented boundary against medical or psychological diagnosis, and recommend professional help when appropriate.

## Reference(s):

- [XinJianXue official website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-parenting-qa-global)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text guidance with HTTP request details and configuration steps when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user consent, dual credentials, paid token balance, and complete subject details before API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
