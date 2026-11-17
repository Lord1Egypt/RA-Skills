## Description:

Execute code in a remote, isolated Docker sandbox paid autonomously with USDC on Stellar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daraijaola](https://clawhub.ai/user/daraijaola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use RunBox when an agent needs to run, test, benchmark, or compute code in a clean remote sandbox across multiple programming languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic mainnet payment can spend real Stellar USDC, and submitted transactions may be irreversible.

Mitigation: Use a dedicated low-balance wallet, prefer testnet for evaluation, and require explicit approval before allowing mainnet payments.

Risk: Code and execution outputs are sent to a third-party remote execution service.

Mitigation: Do not submit secrets, private code, customer data, or other sensitive content; use a trusted self-hosted endpoint when confidentiality matters.

Risk: The default endpoint uses HTTP, and server responses can influence payment details.

Mitigation: Use only endpoints you trust, verify the expected amount and destination before payment, and prefer an HTTPS or self-hosted endpoint.

## Reference(s):

- [RunBox ClawHub Skill Page](https://clawhub.ai/daraijaola/skills/runbox)
- [RunBox Homepage](https://github.com/daraijaola/Runbox)
- [x402 Protocol](https://x402.org)
- [RunBox Capabilities Endpoint](http://46.101.74.170:4001/api/exec/.well-known/runbox.json)
- [Stellar Horizon Mainnet](https://horizon.stellar.org)
- [Stellar Horizon Testnet](https://horizon-testnet.stellar.org)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON execution results with stdout, stderr, exit code, execution time, and optional session metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit code to a remote execution service and may initiate Stellar USDC payments before returning results.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
