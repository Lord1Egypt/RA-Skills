## Description:

XinJianXue Roommate Relations Advisor helps agents provide roommate boundary-negotiation guidance after user consent and authenticated API onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they want roommate conflict guidance focused on negotiating boundaries, conversation timing, and standing rules. The agent must confirm consent before analysis and must only analyze the user or another person the user explicitly mentioned and agreed to analyze.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends birth, gender, and location details to XinJianXue for processing.

Mitigation: Confirm the user understands and agrees before analysis, collect only the required fields, and do not store returned reports.

Risk: The skill requires a sensitive one-time authorization code and persistent service credentials.

Mitigation: Use the authorization code only for account binding, never reveal license or API keys in chat, and store credentials only in an OS keychain, credential manager, or another agreed secure location.

Risk: Report calls can consume the user's account tokens.

Mitigation: Tell the user that calls are token-billed before starting and only check billing details when the user asks.

## Reference(s):

- [XinJianXue website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-roommate-global)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and credential-handling steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user consent, authenticated XinJianXue credentials, and direct HTTP capability; reports can consume account tokens.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
