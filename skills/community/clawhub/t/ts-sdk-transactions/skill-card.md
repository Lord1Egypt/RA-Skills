## Description:

Guides agents through building, signing, submitting, waiting for, and simulating standard, sponsored, and multi-agent Aptos transactions with @aptos-labs/ts-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate Aptos TypeScript SDK transaction guidance and code examples for build, sign, submit, wait, simulation, fee-payer, and multi-agent flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction examples can be adapted to sign or submit transactions with real accounts.

Mitigation: Confirm the target network, module address, function, arguments, and signer accounts before signing or submitting, especially on mainnet.

Risk: High-value or risky transactions may fail or consume unexpected gas if submitted without checking execution behavior first.

Mitigation: Simulate critical flows first, inspect success, vm_status, and gas usage, and prefer testnet or devnet during development.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iskysun96/skills/ts-sdk-transactions)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
