## Description:

进销存 ERP —— 采购入库、销售出库、库存查询、成本核算、报表，全程 AI 对话驱动。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lan202509](https://clawhub.ai/user/lan202509)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and operators use this skill to configure an MCP-backed inventory ERP workflow, create organizations and users, and manage purchasing, sales, inventory, costing, reports, warehouses, items, suppliers, and customers through natural-language agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to persist external MCP access and manage bearer tokens for ERP data.

Mitigation: Install only when the publisher is trusted with ERP data, review MCP configuration changes manually, and avoid pasting or logging token-bearing configuration.

Risk: The skill can guide changes to quantities, approvals, reversals, retries, and other business records.

Mitigation: Require explicit confirmation before the agent changes quantities, approvals, reversals, or other business records.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/lan202509/skills/xiaolan-erp)
- [Xiaolan ERP MCP endpoint](https://xiaolan-tech.com/mcp/erp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with JSON MCP configuration and structured tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bearer-token MCP headers after setup; token-bearing configuration should be handled carefully.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
