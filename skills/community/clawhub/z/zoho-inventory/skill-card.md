## Description:

Helps agents manage Zoho Inventory records through an authorized account, including items, orders, invoices, bills, contacts, and shipments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Inventory and operations teams use this skill to look up and, with approval, update Zoho Inventory items, contacts, sales and purchase orders, invoices, bills, and shipments. Users can also approve scheduled or event-driven actions on their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to inventory, orders, invoices, or other business records may have financial or operational consequences.

Mitigation: Prefer read-only access; verify the account and target record, and obtain explicit approval for every write or deletion.

Risk: Approved automations can run repeatedly and send event data to external destinations.

Mitigation: Confirm each automation and destination, limit the data forwarded, and avoid third-party destinations unless the user understands the ongoing data flow.

Risk: Exposed credentials or broad permissions could disclose business data.

Mitigation: Use only the necessary account and scopes, keep credentials out of outputs and destinations, and revoke unused connections.

## Reference(s):

- [Zoho Inventory API documentation](https://www.zoho.com/inventory/api/v1/introduction/)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton website](https://maton.ai)
- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/zoho-inventory)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with command, code, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Zoho Inventory business records through the authorized connection.]

## Skill Version(s):

1.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
