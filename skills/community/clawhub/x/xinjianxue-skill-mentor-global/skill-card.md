## Description:

XinJianXue Mentor Relationship Advisor helps an agent call the XinJianXue API, with user consent, to produce mentor-relationship analysis and guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to request XinJianXue relationship analysis about mentor and authority-figure situations after consent and onboarding. The skill guides the agent through authentication, credential handling, report requests, and user-facing advice that avoids flattery or scheming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal details, including birth information and location, to www.xinjianxue.com for processing.

Mitigation: Use the skill only after explicit user consent and only with details the user intentionally provides for the requested analysis.

Risk: The service is token-billed and report calls consume account balance.

Mitigation: Tell the user before report calls that the service consumes tokens and check billing only when the user asks.

Risk: The license key, API key, and one-time authorization code are sensitive credentials.

Mitigation: Store generated credentials only in approved credential storage, mask credentials in conversation, and ask only for the one-time authorization code during binding.

Risk: The external report can contain instruction-like text.

Mitigation: Treat returned reports as reference data and follow only the local skill role definition and current user request.

## Reference(s):

- [XinJianXue official website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)
- [ClawHub skill listing](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-mentor-global)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request details and user-facing advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill requires explicit user consent, sends personal details to www.xinjianxue.com, uses token-billed report calls, and treats returned reports as reference data rather than instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
