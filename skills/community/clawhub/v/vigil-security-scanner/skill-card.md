## Description:

Onchain security scanner on Base - scan token approvals, detect honeypots, analyze contracts for rugpull indicators, and score contract safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vigilcodes](https://clawhub.ai/user/vigilcodes)

### License/Terms of Use:

MIT-0

## Use Case:

External DeFi users and developers use this skill to scan Base wallets and token contracts for risky approvals, honeypot behavior, rugpull indicators, market context, deployer reputation, scam reports, and safety scores before trading or auditing a wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes revocation and scam-report scripts that can initiate state-changing workflows, even though the main skill is positioned as read-only scanning.

Mitigation: Use the read-only scan scripts for normal audits. Separately review write scripts and require explicit user approval plus Bankr authentication before revocation or report submission.

Risk: Remote VIGIL lookups send wallet or token addresses to the VIGIL service.

Mitigation: Install and run the skill only when the user intends to trust VIGIL remote lookups for the target addresses being scanned.

Risk: The bundled run script sources a local .env file before startup.

Mitigation: Do not run scripts/run.sh with an untrusted .env file present; review environment variables and secrets before execution.

## Reference(s):

- [VIGIL API Reference](references/api-reference.md)
- [VIGIL Bankr Integration Guide](references/bankr-integration.md)
- [VIGIL Contract Addresses](references/contracts.md)
- [ClawHub Skill Page](https://clawhub.ai/vigilcodes/skills/vigil-security-scanner)
- [VIGIL MCP API Endpoint](https://mcp.vigil.codes/tools/call)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash snippets; script output is terminal text and JSON from the VIGIL API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid 0x address target. Read-only scans call the remote VIGIL endpoint; revoke and scam-report scripts are state-changing workflows that require separate approval.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
