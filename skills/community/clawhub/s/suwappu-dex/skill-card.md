## Description: <br>
Cross-chain token swaps, quotes, portfolio and prices across 14 chains via the Suwappu DEX MCP server. Read-only by default; swap execution is opt-in and gated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xsoftboi](https://clawhub.ai/user/0xsoftboi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Suwappu's hosted MCP server for cross-chain quotes, prices, portfolio views, token lists, and opt-in swap execution after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial trading actions can move funds if swap execution is intentionally enabled. <br>
Mitigation: Keep the default read-only setup unless swaps are required, use a dedicated trading agent or wallet with spending limits, and require user approval before executing a quoted swap. <br>
Risk: A stale or misunderstood route could lead to unfavorable pricing, fees, or chain selection. <br>
Mitigation: Verify every quote, route, price impact, gas estimate, and quote_id with the user before any execute_swap call. <br>
Risk: Exposure of SUWAPPU_API_KEY could allow unauthorized use of the integration. <br>
Mitigation: Store SUWAPPU_API_KEY only as an environment variable or secret and keep it out of committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xsoftboi/suwappu-dex) <br>
- [Suwappu homepage](https://suwappu.bot) <br>
- [Suwappu API documentation](https://api.suwappu.bot/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUWAPPU_API_KEY; the default setup is read-only and excludes execute_swap unless a user intentionally enables trading.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
