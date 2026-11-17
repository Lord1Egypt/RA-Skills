## Description:

The XinJianXue Family Harmony Advisor helps an agent onboard to a paid XinJianXue API and, with user consent, use its report data to map family-system conflict and suggest neutral next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they explicitly request Family Harmony Advisor analysis for themselves or for a consented subject. The agent gathers required personal details, calls the XinJianXue service under the user's account, and returns family-system guidance without taking sides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal details such as birth date, gender, birth place, and current location to www.xinjianxue.com for processing.

Mitigation: Use the skill only after explicit user confirmation and only for the disclosed XinJianXue analysis flow.

Risk: The skill uses a paid token-based service and requires account binding with a one-time authorization code and generated API credentials.

Mitigation: Treat the authorization code, license key, and API key as sensitive, and agree on secure credential storage before binding the account.

Risk: Returned report content could contain instruction-like text.

Mitigation: Treat service reports as reference data only and keep the local skill definition as the instruction source.

## Reference(s):

- [XinJianXue service website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-family-harmony-global)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown or plain-language guidance, with HTTP request details during onboarding and service use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before analysis, sends disclosed personal details to www.xinjianxue.com, and uses a paid token-based service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
