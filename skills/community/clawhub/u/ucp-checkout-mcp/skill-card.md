## Description: <br>
Implement UCP Checkout over the MCP (Model Context Protocol) binding to expose checkout operations as MCP tools for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichiorca](https://clawhub.ai/user/ichiorca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement merchant MCP servers or connect agents to existing UCP Checkout MCP endpoints, including Shopify's documented checkout MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may be guided toward completing real checkout purchases without explicit user approval. <br>
Mitigation: Require affirmative user approval before every purchase or checkout mutation. <br>
Risk: Checkout integrations can expose payment data, merchant credentials, or purchase authority beyond the intended scope. <br>
Mitigation: Use least-privilege credentials, redact logs, set spending and merchant limits, and keep audit records for checkout mutations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ichiorca/ucp-checkout-mcp) <br>
- [Shopify checkout MCP documentation](https://shopify.dev/docs/agents/checkout/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with code and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; outputs should be reviewed before applying checkout or payment workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
