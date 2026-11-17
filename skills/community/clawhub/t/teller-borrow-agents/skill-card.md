## Description:

Expose the Teller delta-neutral + lending Model Context Protocol server so agents can fetch opportunities, borrow terms, and on-chain transaction builders for Teller.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rbcp18](https://clawhub.ai/user/rbcp18)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to install, run, or update a Teller MCP server that exposes delta-neutral opportunity discovery, borrow pool lookup, wallet-specific loan terms, and borrow or repay transaction builders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Borrow and repay builders can return ready-to-submit blockchain transactions that may move assets or create loan obligations if signed without review.

Mitigation: Require explicit human approval and independently verify the chain, destination contracts, calldata, amounts, allowances, and native value before any wallet signs or submits a transaction.

Risk: Using an untrusted or misconfigured Teller API endpoint can expose agents to incorrect transaction data.

Mitigation: Run the skill only against a trusted Teller API endpoint and review any TELLER_API_BASE_URL override before use.

Risk: Wallet addresses and loan IDs are sensitive financial metadata.

Mitigation: Limit where these values are logged, displayed, or shared, and avoid sending them to unnecessary agent tools or services.

Risk: Dependencies may need constraint or update review before production use.

Mitigation: Review, update, or pin the Node dependencies before deploying the MCP server in production.

## Reference(s):

- [Teller Delta-Neutral + Lending API Cheat Sheet](references/delta-neutral-api.md)
- [Teller Delta-Neutral API](https://registry.scalar.com/@teller/apis/delta-neutral/latest)
- [ClawHub Skill Page](https://clawhub.ai/rbcp18/skills/teller-borrow-agents)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool responses containing text summaries plus structured JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tools can return ready-to-submit borrow and repay transaction data from a configured Teller API endpoint.]

## Skill Version(s):

0.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
