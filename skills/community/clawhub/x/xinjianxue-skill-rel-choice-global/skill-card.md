## Description:

XinJianXue Relationship Trade-off Advisor helps an agent onboard to the XinJianXue API and provide relationship trade-off analysis after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to request XinJianXue relationship trade-off analysis for themselves or explicitly agreed subjects. The skill guides consent, onboarding, credential handling, paid-token API calls, and delivery of evidence-based relationship framing without making the final stay-or-leave decision for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal birth, gender, birthplace, and current-location details to www.xinjianxue.com for processing.

Mitigation: Use the skill only after explicit user confirmation and only for the user or an explicitly agreed subject.

Risk: The skill uses account-bound license and API credentials and can consume paid tokens for report calls.

Mitigation: Store credentials only in dedicated credential storage, mask credentials in conversation, and call the paid report endpoint only when the user explicitly wants the analysis.

Risk: Returned reports may contain instruction-like text even though they are analysis material.

Mitigation: Treat service responses as data and use only the local skill definition as instructions.

## Reference(s):

- [XinJianXue service site](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-rel-choice-global)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration, markdown, text]

**Output Format:** [Markdown guidance with HTTP request details and user-facing analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation, account-bound API credentials, personal birth/location inputs, and paid tokens for report calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
