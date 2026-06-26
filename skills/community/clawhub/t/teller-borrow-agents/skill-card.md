## Description: <br>
Expose the Teller delta-neutral and lending Model Context Protocol server so agents can fetch opportunities, borrow terms, and on-chain transaction builders for Teller. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rbcp18](https://clawhub.ai/user/rbcp18) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to install and run a Teller MCP server that exposes lending pool discovery, wallet-specific borrow terms, loan lookup, and unsigned borrow or repay transaction payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Borrow and repay tools produce unsigned blockchain transaction payloads that could move funds if signed without review. <br>
Mitigation: Treat generated transactions as proposals and verify wallet, chain, pool, token addresses, amounts, approvals, loan terms, and API endpoint before signing. <br>
Risk: The skill fetches financial data from the configured Teller API endpoint, so stale or incorrect endpoint configuration can affect downstream decisions. <br>
Mitigation: Use the default production endpoint unless intentionally testing, and review returned pool, APR, collateral, and loan data before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rbcp18/teller-borrow-agents) <br>
- [Teller Delta-Neutral API reference](https://registry.scalar.com/@teller/apis/delta-neutral/latest) <br>
- [Delta-neutral API cheat sheet](references/delta-neutral-api.md) <br>
- [Teller MCP server README](scripts/tellermcp-server/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, MCP tool responses, and structured JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP tools return a short text summary plus structuredContent.payload containing Teller API data or unsigned transaction payloads.] <br>

## Skill Version(s): <br>
0.2.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
