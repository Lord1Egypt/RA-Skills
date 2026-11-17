## Description:

Security Defense Line is a third-party crypto security skill for smart contract checks, wallet and transaction risk review, phishing detection, multisig workflows, and incident response guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External crypto users and developers use this skill to generate security-oriented checks, reports, command guidance, and configuration examples for contracts, wallets, transactions, phishing risks, multisig operations, and incident handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact presents critical crypto protections while the security evidence reports mock or random security results.

Mitigation: Use outputs only as preliminary guidance; verify findings with maintained security tools and qualified human review before wallet, contract, transaction, or incident-response decisions.

Risk: The security evidence reports under-scoped billing behavior with a hardcoded billing credential and potential immediate charging during payment verification.

Mitigation: Review payment behavior before installation, replace hardcoded credentials with environment-managed secrets, and require explicit user consent before charges.

Risk: The artifact documents a security_monitor.py workflow, but that script is not present in the release evidence.

Mitigation: Confirm available files before relying on monitoring workflows and avoid treating missing commands as supported release functionality.

## Reference(s):

- [Security Defense Line on ClawHub](https://clawhub.ai/shenmeng/skills/shenmeng-security-defense-line)
- [Smart Contract Security Auditing Technical Manual](references/contract-auditing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, CLI-oriented text reports, code snippets, shell commands, and JSON-like script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid SkillPay flow is described as 0.01 USDT per call; security outputs require independent review before operational use.]

## Skill Version(s):

2025.4.15 (source: server release evidence; artifact _meta.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
