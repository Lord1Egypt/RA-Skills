## Description:

Matches C+ service opportunities by reading tenant visit records and customer profiles from an Excel ledger, extracting tenant needs, and preparing service recommendations for property managers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Property management and tenant service teams use this skill to analyze recent tenant visit records, identify service needs, match C+ service resources, and prepare follow-up recommendations for manager confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads identifiable tenant and business records from an Excel ledger and may include tenant or contact details in recommendations or notifications.

Mitigation: Use only after business-owner approval, minimize or mask tenant and contact details, and restrict access to approved operators and recipients.

Risk: The skill can send recommendations through a WeCom webhook.

Mitigation: Configure webhook recipients carefully and verify destination and content before enabling scheduled or automated notifications.

Risk: The skill includes scheduled daily analysis and Excel write-back follow-up behavior.

Mitigation: Require explicit operator approval before updating source records and verify the ledger path and write-back fields before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/service-matching)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown or plain text with structured recommendation lists and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations may include tenant profile details, service priorities, suggested discounts, follow-up status, and notification content.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
