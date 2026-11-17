## Description:

Expose the Teller delta-neutral + lending Model Context Protocol server so agents can fetch opportunities, borrow terms, and on-chain transaction builders for Teller.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rbcp18](https://clawhub.ai/user/rbcp18)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to install and run a Teller MCP server that exposes lending pool discovery, wallet-specific borrow terms, loan lookup, and borrow or repayment transaction builders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet lookups and loan data can expose sensitive financial workflow details.

Mitigation: Use the skill only with intended wallets and avoid sharing returned lending data outside the authorized agent session.

Risk: Borrow and repayment builders can produce transaction calldata that moves assets or grants approvals.

Mitigation: Review chain IDs, token addresses, pool addresses, amounts, approval targets, and calldata before signing or submitting any transaction.

Risk: The bundled MCP server depends on an npm dependency set that may change security posture over time.

Mitigation: Audit or update dependencies before running the server in a sensitive environment.

## Reference(s):

- [Teller Delta-Neutral + Lending API Cheat Sheet](references/delta-neutral-api.md)
- [Teller Delta-Neutral API Documentation](https://registry.scalar.com/@teller/apis/delta-neutral/latest)
- [ClawHub Skill Page](https://clawhub.ai/rbcp18/skills/teller-borrow)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool responses containing text plus structured JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP tools may return wallet-linked lending data and encoded on-chain transaction calldata.]

## Skill Version(s):

0.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
