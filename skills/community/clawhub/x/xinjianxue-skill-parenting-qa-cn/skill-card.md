## Description:

A Chinese parenting Q&A advisor skill that helps agents answer parent-child relationship questions using explicit user consent, an authenticated Xinjianxue API report, and locally defined parenting-guidance roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they explicitly want parenting relationship guidance, such as help discussing communication breakdowns, adolescence, or academic decline with a child. The agent gathers consent and required personal details, calls the Xinjianxue report API, and turns the returned report data into practical communication guidance without replacing medical or psychological diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal birth, gender, and location details to an external service and each report may consume credits.

Mitigation: Use it only after explicit user consent, confirm the disclosed domain, and explain credit use before requesting personal details.

Risk: The setup flow handles a one-time authorization code and generated API credentials.

Mitigation: Ask only for the one-time authorization code, store generated credentials in dedicated secret storage, and mask credentials in conversation or logs.

Risk: Returned report content could contain text that looks like instructions.

Mitigation: Treat API reports as data and reference material only; follow the local skill instructions for behavior.

## Reference(s):

- [Xinjianxue API base](https://chinaapi.xinjianxue.com)
- [Xinjianxue API path prefix](https://chinaapi.xinjianxue.com/api/xinjianxue)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-parenting-qa-cn)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text parenting guidance based on API-returned report data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user consent, one-time account binding, protected credential storage, and user-provided birth, gender, and location details before report generation.]

## Skill Version(s):

2.1.1 (source: ClawHub server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
