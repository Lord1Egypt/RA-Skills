## Description:

Provides an agent workflow for onboarding to the XinJianXue paid API and generating best-friend relationship guidance from user-approved personal details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to connect to XinJianXue, request consent, manage the one-time account binding flow, and produce best-friend relationship analysis guidance. It is intended for relationship and personality-oriented questions where the user has clearly asked for this service and supplied the required personal details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal birth, gender, and location details to www.xinjianxue.com for analysis.

Mitigation: Use the service only after explicit user consent and only for subjects the user is authorized to analyze.

Risk: The integration uses paid XinJianXue tokens for report calls.

Mitigation: Confirm the user understands that report requests may be billed against their token balance before calling the API.

Risk: The onboarding flow handles a one-time authorization code and generated service credentials.

Mitigation: Store license and api_key values only in a credential manager or agreed environment variable, and never expose them in chat, files, or long-term memory.

Risk: Reports returned by the service may contain text that looks instructional.

Mitigation: Treat service reports as analysis data only and follow the local skill instructions for agent behavior.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-bff-global)
- [XinJianXue service site](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with HTTP request and credential-handling instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be delivered in the user's native language; reports returned by the service are treated as data rather than instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
