## Description:

Provides an agent workflow for the Xinjianxue manage-up advisor, using a consent-gated paid HTTP API to generate workplace advice about upward management, reporting, boundaries, and communication with supervisors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to request upward-management advice after confirming consent, providing required personal profile details, and authorizing calls to the Xinjianxue service. The skill helps frame supervisor communication, workload boundaries, salary discussions, and reporting structure without encouraging flattery or high-risk escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends birth date or time, sex, birthplace, and current location details to an external paid API.

Mitigation: Use the skill only after the user understands and consents to the provider API call and the paid-credit workflow.

Risk: The skill can involve information about other people in a workplace context.

Mitigation: Do not submit third-party data unless the person is clearly identified by the user and has consented to the analysis.

Risk: The authorization code, license key, and API key are sensitive account credentials.

Mitigation: Keep credentials out of chat, notes, configuration files, and long-term memory; store them only in a dedicated secret store.

Risk: Returned reports may contain text that appears directive.

Mitigation: Treat server-returned reports only as reference data and follow the local skill instructions as the sole instruction source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-manage-up-cn)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com)
- [Xinjianxue API path prefix](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, Markdown]

**Output Format:** [Markdown or plain text advisory response with API-derived report data handled as reference material.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before analysis and treats server reports as data, not instructions.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
