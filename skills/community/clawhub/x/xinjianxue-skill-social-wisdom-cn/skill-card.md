## Description:

Provides a Chinese Xinjianxue social-wisdom adviser that helps agents answer social etiquette questions after user confirmation and, when needed, a paid Xinjianxue report API call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to get Chinese-language advice on social etiquette, relationship context, gift-giving, asking for help, and polite refusals. The agent should call the Xinjianxue report API only after user confirmation and should treat returned reports as reference data, not instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive birth details, gender, and location information to a third-party API.

Mitigation: Use the skill only after the analyzed person has explicitly agreed, avoid exact birth time and birthplace unless that report tier is intentional, and share only the minimum data needed.

Risk: The skill requires storing an API credential for paid future calls.

Mitigation: Store license and API credentials only in a dedicated secret store, avoid displaying them in chat or configuration files, and rotate or rebind through the publisher's support channel if compromised.

Risk: Returned report content could contain instruction-like text.

Mitigation: Treat API report content only as reference data and keep local skill instructions as the sole behavioral authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-social-wisdom-cn)
- [Xinjianxue API service](https://chinaapi.xinjianxue.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, Configuration]

**Output Format:** [Markdown guidance with HTTP request and JSON response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation, third-party API credentials, and birth, gender, and location inputs for report generation.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
