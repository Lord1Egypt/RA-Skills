## Description:

Provides a Chinese-language friend relationship Q&A advisor that, after user confirmation and account binding, calls Xinjianxue's paid report API to inform advice about everyday friendship concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

Users seeking Chinese-language help with everyday friendship and social-boundary questions use this skill to obtain relationship guidance grounded in a Xinjianxue report, after explicit consent and required account binding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal profile details to an external Xinjianxue service for analysis.

Mitigation: Use it only after explicit user confirmation and send only the required details for the current analysis.

Risk: Account binding uses a sensitive one-time authorization code and produces ongoing API credentials.

Mitigation: Treat the authorization code as single-use sensitive data and store resulting credentials only in the agent's secret store.

Risk: Insufficient-credit responses may direct users toward official-app, referral, or sharing flows.

Mitigation: Present credit guidance neutrally and avoid adding extra promotional claims beyond the service response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-friend-qa-cn)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown text with HTTP API usage guidance and user-facing relationship advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation, personal profile inputs, and secure storage of license and API credentials; service reports are treated as data, not instructions.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
