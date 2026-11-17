## Description:

Use when an agent needs to store, retrieve, list, inspect, or delete files through Vaultline, or when it needs to choose between open and private storage tiers, construct the required wallet-auth headers for private objects, or follow the x402 pay-and-retry flow for uploads and downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to integrate with Vaultline file storage, choose an open or private tier, construct wallet-authenticated requests, and follow x402 payment retry flows for uploads and downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may upload sensitive data to the open tier, making it readable to anyone with the path who satisfies payment requirements.

Mitigation: Require an explicit open or private tier choice before upload, and use private storage for internal, customer-sensitive, or wallet-restricted data.

Risk: Payment retries could sign an unintended x402 payment payload if the amount, operation, or target is not checked.

Mitigation: Confirm the operation, target path, and payment amount before signing and retry the same original request only after validation.

Risk: Delete and private-access operations can affect protected objects or expose wallet authentication material.

Mitigation: Confirm the exact delete target before execution and treat wallet headers, signatures, and signed auth messages as sensitive.

Risk: The npm SDK dependency may change over time and affect reproducibility.

Mitigation: Review or pin the @builtbyecho/vaultline-sdk dependency when deterministic behavior is required.

## Reference(s):

- [Vaultline API Examples](references/api-examples.md)
- [Pricing and Tier Selection](references/pricing-and-tier-selection.md)
- [Vaultline GitHub Repository](https://github.com/BuiltByEcho/vaultline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline HTTP examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Vaultline request headers, tier-selection guidance, x402 payment retry steps, and API usage examples.]

## Skill Version(s):

0.1.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
