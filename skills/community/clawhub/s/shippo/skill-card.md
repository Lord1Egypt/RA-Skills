## Description:

A shipping and logistics skill for Shippo that helps agents get multi-carrier rates, buy domestic and international labels with customs, validate addresses, track packages, run CSV batches, analyze costs, route integrations, and support SDK upgrades through Shippo's hosted OAuth MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shippo](https://clawhub.ai/user/shippo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and shipping operations teams use this skill to compare carrier rates, validate addresses, purchase Shippo labels, prepare customs details, track shipments, process batch CSV shipments, and troubleshoot Shippo integrations through the hosted OAuth MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live label purchases, batch purchases, refunds, webhook changes, and deletion actions that affect a real Shippo account.

Mitigation: Require explicit user approval for write actions and review carrier, service, cost, ETA, refund, webhook, or deletion details before proceeding.

Risk: Shipment, contact, customs, and tracking details may be sent to Shippo and carriers or included in local analysis reports at the user's request.

Mitigation: Minimize personal information in generated reports and confirm that the user is comfortable connecting their Shippo account through OAuth before use.

## Reference(s):

- [Project homepage](https://github.com/goshippo/ai)
- [Shippo hosted MCP](https://mcp.shippo.com)
- [API Concepts](https://docs.goshippo.com/docs/api_concepts/apiversioning)
- [Address Validation Guide](https://docs.goshippo.com/docs/addresses/address_validation)
- [Customs Reference](https://docs.goshippo.com/docs/exporting/internationalshipments)
- [Carrier Accounts](https://docs.goshippo.com/docs/shipping/carrieraccounts)
- [Webhooks](https://docs.goshippo.com/docs/tracking/webhooks)
- [API Changelog](https://docs.goshippo.com/changelog)
- [Carrier Guide](references/carrier-guide.md)
- [CSV Batch Format Specification](references/csv-format.md)
- [Customs Declaration Guide](references/customs-guide.md)
- [Shippo MCP Operation Reference](references/tool-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API Calls, Files]

**Output Format:** [Markdown guidance with JSON snippets, API-operation instructions, and optional CSV or Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local analysis reports and CSV files when the user asks for shipping analysis.]

## Skill Version(s):

1.4.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
