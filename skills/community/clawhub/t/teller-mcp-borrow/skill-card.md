## Description:

Expose the Teller delta-neutral and lending Model Context Protocol server so agents can fetch opportunities, borrow terms, and on-chain transaction builders for Teller.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rbcp18](https://clawhub.ai/user/rbcp18)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to install and run an MCP server that exposes Teller lending, delta-neutral opportunity, loan, borrow transaction, and repayment tools to MCP-compatible agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can return remotely supplied blockchain transaction payloads for borrowing or repayment.

Mitigation: Before signing, independently verify the chain, contract address, spender, calldata, token amounts, native value, loan terms, and repayment details.

Risk: The configured Teller API endpoint receives wallet-linked borrowing parameters.

Mitigation: Keep TELLER_API_BASE_URL fixed to a trusted HTTPS endpoint and avoid sending wallet-linked borrowing data to untrusted instances.

Risk: Evidence reports that vulnerable dependencies should be updated before production use.

Mitigation: Update dependencies, rebuild the MCP server, and retest before production deployment.

## Reference(s):

- [Teller Delta-Neutral + Lending API Cheat Sheet](references/delta-neutral-api.md)
- [Teller Delta-Neutral API Reference](https://registry.scalar.com/@teller/apis/delta-neutral/latest)
- [ClawHub Skill Page](https://clawhub.ai/rbcp18/skills/teller-mcp-borrow)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [MCP tool responses with text summaries and structured JSON payloads, plus Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns unsigned transaction payloads that require independent review before signing.]

## Skill Version(s):

0.1.6 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
