## Description:

Monitor supplier APIs, port delays, and weather in real time to trigger automatic PO rerouting and stakeholder alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Supply chain, procurement, and logistics teams use this skill to monitor supplier, shipment, port, weather, and ERP signals for disruption risk. It helps produce rerouting recommendations, purchase-order workflows, stakeholder alerts, supplier health reports, and ETA updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create purchase orders, update ERP records, and send stakeholder notifications using broad business credentials.

Mitigation: Use least-privilege credentials, start in monitoring or dry-run mode, and require explicit approval before spending, ERP writes, or customer-facing messages.

Risk: Stored supplier and integration credentials could expose logistics, database, notification, or ERP systems if mishandled.

Mitigation: Store credentials in a secret manager and avoid placing supplier credentials directly in the supplier table.

Risk: Automatic rerouting can make operational decisions based on delayed or inaccurate supplier, AIS, weather, or logistics data.

Mitigation: Use conservative thresholds, keep redundant data sources where possible, and review recommendations before enabling automated PO creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/supplychainsentinel)
- [Publisher profile](https://clawhub.ai/user/ncreighton)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, SQL, YAML, shell commands, and notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference live logistics, weather, database, notification, and ERP credentials when the required integrations are configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
