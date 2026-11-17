## Description:

Send global bulk SMS with two-way replies and monitor delivery status for cross-border business outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales, operations, and customer support teams use this skill to send paid bulk SMS, enable two-way replies, and review delivery records for cross-border outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send paid SMS messages and may incur charges.

Mitigation: Require explicit user confirmation before paid send operations and use current pricing or account balance information before execution.

Risk: The API key may be exposed if passed on the command line or stored with broad filesystem permissions.

Mitigation: Prefer UPKUAJING_API_KEY in the environment or a restricted ~/.upkuajing/.env file and avoid echoing or logging secrets.

Risk: SMS workflows can expose phone numbers, message bodies, or secrets in troubleshooting reports.

Mitigation: Use the error-reporting flow only after user confirmation and omit sensitive data unless needed.

Risk: The skill can be misused for unwanted or unlawful messaging.

Mitigation: Use only for lawful, consent-based SMS workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/upkuajing-sms-tool)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [SMS Send API](artifact/references/sms-send-api.md)
- [SMS Task List API](artifact/references/sms-task-list-api.md)
- [SMS Task Record List API](artifact/references/sms-task-record-list-api.md)
- [Skill Error Report API](artifact/references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return SMS task identifiers, delivery counts, delivery statuses, pricing or balance details, and request IDs.]

## Skill Version(s):

1.0.4 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
