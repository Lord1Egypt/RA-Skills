## Description:

Helps ecommerce sellers use YunExpress and Yanwen APIs to track parcels, compare rates, prepare carrier orders and labels, and review state-changing shipping actions before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvsao](https://clawhub.ai/user/lvsao)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers and operations teams use this skill to query carrier-side YunExpress and Yanwen shipment data, quotes, channels, labels, and order status. They can also prepare shipment or account-state changes with a redacted preview and explicit approval before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Carrier credentials and parcel data can be sent over insecure or insufficiently restricted API destinations.

Mitigation: Use only official carrier hosts, prefer HTTPS where available, and avoid production credentials unless the endpoint and environment are verified.

Risk: State-changing carrier actions can create, cancel, alter, or subscribe real shipment and account records.

Mitigation: Review every redacted preview, require explicit user approval before execution, and verify the affected waybill or subscription after the request.

Risk: Environment files contain carrier account codes and API secrets.

Mitigation: Keep generated env files private, ignored by version control, and protected with restrictive local permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvsao/skills/yuntu-yw-shipping)
- [Project homepage](https://github.com/lvsao/shopify-skill-hub)
- [Yanwen API reference](references/yanwen-api.md)
- [YunExpress API reference](references/yunexpress-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local carrier credentials; write operations should show redacted previews and require explicit approval before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
