## Description:

Exposes a Teller Model Context Protocol server so agents can fetch delta-neutral opportunities, borrow pools and terms, wallet loans, and encoded borrow or repay transaction builders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rbcp18](https://clawhub.ai/user/rbcp18)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to install, run, or update a Teller MCP server that exposes lending, loan, and delta-neutral opportunity data to MCP-compatible agents. It is suited for workflows that need structured Teller API results and unsigned borrow or repayment transaction proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Borrow and repay tools can produce high-impact on-chain transaction proposals with insufficient user-safety controls.

Mitigation: Decode each proposed transaction and verify contracts, spenders, amounts, chain IDs, and native values before any wallet signs or submits it.

Risk: Wallet-connected or automated trading environments may act on unsafe or unexpected transaction-builder output.

Mitigation: Require explicit human approval for borrow and repayment transactions and treat all returned calldata as untrusted until independently reviewed.

Risk: A malicious or misconfigured Teller API base URL could affect returned lending data or transaction proposals.

Mitigation: Use only a trusted TELLER_API_BASE_URL and audit or update dependencies before deployment.

## Reference(s):

- [Teller Delta-Neutral + Lending API Cheat Sheet](references/delta-neutral-api.md)
- [Teller Delta-Neutral API Reference](https://registry.scalar.com/@teller/apis/delta-neutral/latest)
- [ClawHub Skill Page](https://clawhub.ai/rbcp18/skills/tellermcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell and configuration snippets; MCP tool responses contain text summaries plus structured JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Borrow and repay transaction-builder outputs are unsigned transaction proposals that require wallet-side review before signing or submission.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
