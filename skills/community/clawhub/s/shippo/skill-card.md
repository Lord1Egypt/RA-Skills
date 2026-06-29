## Description: <br>
A shipping and logistics skill for Shippo that helps agents get multi-carrier rates, buy domestic and international labels with customs, validate addresses, track packages with webhooks, run bulk CSV batches, analyze shipping costs, route integrations, and support SDK upgrades through Shippo's hosted OAuth MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shippo](https://clawhub.ai/user/shippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and shipping teams use this skill to connect an agent to Shippo for rate shopping, address validation, label purchasing, tracking, batch shipping, customs workflows, shipping-cost analysis, and integration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects through OAuth to a Shippo account and can access shipping, address, tracking, and account configuration data. <br>
Mitigation: Use only an intended Shippo account, keep OAuth access scoped to the user session, and treat returned shipping and account data as operational data. <br>
Risk: Write operations can buy labels, request refunds, delete or change webhooks, and modify carrier-account settings. <br>
Mitigation: Require explicit user confirmation before purchases, refunds, deletions, webhook changes, carrier-account changes, or any other write operation. <br>
Risk: Analysis workflows may save markdown and CSV reports locally in an analysis/ directory. <br>
Mitigation: Handle generated reports as operational records and avoid sharing or retaining them beyond the user's workflow needs. <br>


## Reference(s): <br>
- [Shippo AI GitHub Homepage](https://github.com/goshippo/ai) <br>
- [Shippo Hosted MCP](https://mcp.shippo.com) <br>
- [API Concepts](https://docs.goshippo.com/docs/api_concepts/apiversioning) <br>
- [Address Validation Guide](https://docs.goshippo.com/docs/addresses/address_validation) <br>
- [Customs Reference](https://docs.goshippo.com/docs/exporting/internationalshipments) <br>
- [Carrier Accounts](https://docs.goshippo.com/docs/shipping/carrieraccounts) <br>
- [Webhooks](https://docs.goshippo.com/docs/tracking/webhooks) <br>
- [Carrier Guide](references/carrier-guide.md) <br>
- [CSV Batch Format Specification](references/csv-format.md) <br>
- [Customs Declaration Guide](references/customs-guide.md) <br>
- [Shippo MCP Operation Reference](references/tool-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with JSON configuration snippets, code examples, shell commands, tables, label or tracking links, and optional local markdown/CSV analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Shippo's hosted MCP through per-user OAuth; analysis workflows may create markdown and CSV files under an analysis/ directory.] <br>

## Skill Version(s): <br>
1.4.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
