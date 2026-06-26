## Description: <br>
Maintain or use the read-only revert.wtf MCP server that exposes bounded catalog search, parser, selector lookup, AA explanations, x402 entries, and Blockscout registry tools to agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrtdlgc](https://clawhub.ai/user/mrtdlgc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to maintain MCP behavior, test MCP changes, document agent integration, or help agents consume revert.wtf catalog data for EVM, RPC, provider, wallet, AA, and x402 errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates in crypto and wallet-related contexts where sensitive credentials may be nearby. <br>
Mitigation: Do not provide private keys, wallet seed phrases, session tokens, or live transaction-signing authority to the agent. <br>
Risk: Changing MCP behavior could accidentally expand the server beyond read-only lookup and explanation workflows. <br>
Mitigation: Keep MCP behavior read-only and exclude signing, transaction sending, payment gating, chain calls, browser scraping, and provider fetches. <br>
Risk: Unbounded catalog or chain searches can create inefficient or overly large agent outputs. <br>
Mitigation: Keep search and list tools bounded and paginated, returning summaries first and full entries only after a selected id is requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrtdlgc/revertwtf-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JSON text examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports read-only MCP tool and resource guidance with bounded, paginated lookup behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
