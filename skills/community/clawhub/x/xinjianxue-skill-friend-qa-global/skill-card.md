## Description:

XinJianXue "Friendship & Social Advisor" helps an agent onboard to the XinJianXue service and request user-confirmed friendship and social relationship analyses through its paid HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to obtain XinJianXue friendship and social-advice reports after explicit consent, authentication, and collection of required personal details. It is intended for relationship-analysis guidance, personality and behavior reading, and emotional-support workflows within the Friendship & Social Advisor scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal birth, gender, and location details to a third-party paid API for each confirmed analysis.

Mitigation: Ask for explicit user agreement before each analysis and collect only the required details for the requested report.

Risk: Onboarding and later calls rely on sensitive license and API credentials, plus a one-time authorization code during binding.

Mitigation: Use a dedicated credential store, mask credentials in conversation, and request the authorization code only during the binding step.

Risk: API calls may consume account tokens.

Mitigation: Tell users that analyses are billed in tokens before calling the service and only query billing details when the user asks.

Risk: Returned report text could contain instruction-like content.

Mitigation: Treat returned reports as data and reference material only; follow the local skill instructions for agent behavior.

## Reference(s):

- [XinJianXue official website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-friend-qa-global)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON request examples and HTTP API instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include translated relationship-analysis summaries derived from XinJianXue API report data; returned report content is treated as reference material, not instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
