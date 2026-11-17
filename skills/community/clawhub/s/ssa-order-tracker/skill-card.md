## Description:

Tracks local sales orders with manual status updates, customer email notifications, and command-line dashboard reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Operations staff and agents use this skill to inspect order status, move orders through a fixed fulfillment lifecycle, preview or send customer status emails, and generate dashboard summaries for urgent or overdue orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The notification workflow can send real customer emails and update order records.

Mitigation: Use dry-run mode during testing, require operator review before live sends or writes, and restrict who can execute the scripts.

Risk: The skill reuses SMTP credentials from another skill's .env file.

Mitigation: Use a dedicated SMTP account or managed secret source for this skill instead of reading another skill's credential file.

Risk: Order data and logs may contain customer names, emails, addresses, order values, and shipment information.

Mitigation: Limit filesystem access to the data and log files, avoid sharing generated logs broadly, and sanitize records before using untrusted inputs.

Risk: Mail dependencies and order records may be deployed without enough independent validation.

Mitigation: Verify or update the mail dependencies before deployment and validate order records against the included JSON schema.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cjboy007/skills/ssa-order-tracker)
- [Order Tracker README](artifact/README.md)
- [Agent Skill Definition](artifact/SKILL.md)
- [Order Data JSON Schema](artifact/config/order-schema.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus CLI table, compact text, and JSON output from the included scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local orders JSON data and append local status or notification logs when run outside dry-run mode.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
