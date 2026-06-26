## Description: <br>
Expose the Teller delta-neutral + lending Model Context Protocol server so agents can fetch opportunities, borrow terms, and on-chain transaction builders for Teller. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rbcp18](https://clawhub.ai/user/rbcp18) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to install, run, or update a Teller MCP server that exposes lending, loan, and delta-neutral opportunity tools to MCP-compatible agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Borrow and repayment tools can generate on-chain transaction data that may move assets or grant approvals if signed. <br>
Mitigation: Independently verify the destination, chain, amounts, approvals, and calldata before signing any generated borrow or repayment transaction. <br>
Risk: Using an untrusted Teller API endpoint could return misleading pool, loan, or transaction-builder data. <br>
Mitigation: Use the default Teller endpoint or another endpoint you trust before connecting the MCP server. <br>
Risk: Wallet addresses sent to the MCP server and Teller API may reveal borrowing or loan activity. <br>
Mitigation: Avoid sharing wallet addresses unnecessarily and limit use to wallets appropriate for the lending workflow. <br>


## Reference(s): <br>
- [Teller Delta-Neutral + Lending API Cheat Sheet](references/delta-neutral-api.md) <br>
- [Teller Delta-Neutral API Documentation](https://registry.scalar.com/@teller/apis/delta-neutral/latest) <br>
- [ClawHub Skill Page](https://clawhub.ai/rbcp18/tellermcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP structured JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP tool responses include short text summaries and structuredContent payloads for downstream automation.] <br>

## Skill Version(s): <br>
0.1.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
