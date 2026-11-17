## Description:

Guides agents in creating and configuring the Aptos TypeScript SDK client with AptosConfig, network selection, endpoint overrides, singleton usage, and Bun compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to produce Aptos TypeScript SDK client setup guidance, including reusable client configuration, network selection, custom endpoint handling, and common setup mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using mainnet transaction APIs can cause real state-changing operations.

Mitigation: Confirm the intended Aptos network before applying examples, and default development workflows to testnet unless mainnet use is intentional.

Risk: Faucet funding examples are inappropriate for production or mainnet workflows.

Mitigation: Use faucet funding only in supported devnet or testnet environments.

Risk: Custom endpoint configuration can target the wrong fullnode, indexer, or faucet service.

Mitigation: Set Network.CUSTOM when overriding endpoints and review environment-provided URLs before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iskysun96/skills/ts-sdk-client)
- [Aptos SDK client source reference](src/api/aptos.ts)
- [AptosConfig source reference](src/api/aptosConfig.ts)
- [TypeScript SDK pattern](../../../../patterns/fullstack/TYPESCRIPT_SDK.md)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no hidden execution, persistence, or data collection behavior reported.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
