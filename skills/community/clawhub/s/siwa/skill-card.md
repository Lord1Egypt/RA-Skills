## Description:

SIWA (Sign-In With Agent) authentication for ERC-8004 registered agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buildersgarden](https://clawhub.ai/user/buildersgarden)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add SIWA authentication, wallet signing, server-side verification, ERC-8128 request signing, x402 payment flows, and reverse CAPTCHA handling for ERC-8004 registered agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet signing, payments, and secrets, and the security scan flagged examples with unsafe defaults or missing safeguards.

Mitigation: Review and harden examples before production use; pin package and container versions, require strong secrets without fallback values, and store wallet/provider credentials in a managed secret store.

Risk: State-changing authenticated requests and x402 payment flows can create replay or spending exposure if copied without additional controls.

Mitigation: Require replay protection for state-changing requests, add explicit approval and spending limits for x402 payments, and verify calldata, contract addresses, chain IDs, and gas funding before submitting transactions.

## Reference(s):

- [SIWA Documentation](https://siwa.id/docs)
- [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004)
- [ERC-8128](https://eips.ethereum.org/EIPS/eip-8128)
- [SIWA Specification](references/siwa-spec.md)
- [Security Model](references/security-model.md)
- [ERC-8004 Registration Guide](references/registration-guide.md)
- [ERC-8004 Contract Addresses and ABIs](references/contract-addresses.md)
- [SIWA Sessions vs x402 SIWX](references/siwa-vs-siwx.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet-specific setup paths, server verification examples, registration guidance, and security notes.]

## Skill Version(s):

0.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
