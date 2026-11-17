## Description:

XinJianXue Tailored Teaching Advisor helps an agent collect user-approved birth, gender, and location details, call the XinJianXue paid API, and produce trait-based teaching guidance for a child's learning and parenting questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to onboard to XinJianXue, request consent, submit required subject details, and generate Tailored Teaching Advisor guidance about a child's study habits, tutoring fit, and parent guidance. The skill is scoped to confirmed teaching-advisor questions and should not analyze unmentioned or non-consenting third parties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive birth, gender, and location details to an external XinJianXue service.

Mitigation: Confirm user consent before each analysis, collect only required subject details, and do not use the service for non-consenting third parties.

Risk: Onboarding and report calls use sensitive authorization, license, and API credentials.

Mitigation: Use the authorization code only in the official binding flow and store license and API credentials only in user-agreed credential storage, never in chat or configuration files.

Risk: Each report consumes paid account tokens.

Mitigation: Disclose token use before report calls and check billing details only when the user asks.

Risk: Returned reports may contain instruction-like text.

Mitigation: Treat API reports as data and follow only the local skill role definition and user request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-teach-fit-global)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [XinJianXue service](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, API Calls, Configuration]

**Output Format:** [Markdown guidance with HTTP API request details and credential storage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on a time-sensitive paid API report that must be treated as data, translated for the user when needed, and not stored.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
