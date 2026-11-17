## Description:

Travel Customizer guides travelers through a confirmation-first intake conversation and submits structured travel requirements to a configured Feishu Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijingxu007](https://clawhub.ai/user/lijingxu007)

### License/Terms of Use:

MIT-0

## Use Case:

Travel businesses and travel consultants use this skill to collect customer destination, party size, budget, timing, contact, and preference details through conversation, confirm the summary with the user, and store the lead in Feishu for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer contact details and travel preferences are stored in a configured Feishu table.

Mitigation: Use a dedicated least-privilege Feishu app and table, restrict record access, disclose storage to travelers, and define retention and deletion practices.

Risk: Misconfigured Feishu credentials or table identifiers can prevent submission or expose records to the wrong workspace.

Mitigation: Validate FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_BASE_TOKEN, and FEISHU_TABLE_ID before use, and test with non-sensitive sample records.

Risk: Raw integration errors may expose operational details to users.

Mitigation: Sanitize error messages before displaying them and route detailed diagnostics to administrators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijingxu007/skills/tc-travel)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Conversational text with structured tool parameters submitted to Feishu]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials, base token, and table ID configured as environment variables.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
