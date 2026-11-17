## Description:

Generates Aptos Move V2 smart-contract guidance and code patterns for Object model usage, Digital Asset integration, security checks, and storage type selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Aptos Move smart contracts use this skill to draft modules, NFT collections, marketplaces, staking or DAO components, and storage designs. It provides Aptos Object model, Digital Asset, access-control, event, arithmetic-safety, testing-accessor, and gas-aware storage guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation may cause the skill to influence loosely related or non-Aptos contract-writing requests.

Mitigation: Narrow activation to explicit Aptos or Move smart-contract requests before installation.

Risk: Unsafe examples or incomplete generated logic could lead to vulnerable production smart contracts.

Mitigation: Review and correct examples before relying on generated code, and independently audit and test every contract before deployment.

Risk: Generated code may omit project-specific security controls, storage tradeoffs, or deployment constraints.

Mitigation: Require human review of signer checks, input validation, access control, event coverage, gas and storage decisions, and deployment readiness.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iskysun96/skills/write-contracts)
- [Digital Asset Standard](https://aptos.dev/build/smart-contracts/digital-asset)
- [Object Model](https://aptos.dev/build/smart-contracts/object)
- [Move Security Guidelines](https://aptos.dev/build/smart-contracts/move-security-guidelines)
- [Storage Decision Tree](references/storage-decision-tree.md)
- [Storage Patterns](references/storage-patterns.md)
- [Storage Type Reference](references/storage-types.md)
- [Storage Gas Optimization](references/storage-gas-optimization.md)
- [Object Patterns](references/object-patterns.md)
- [Access Control Patterns](references/access-control.md)
- [Safe Arithmetic Patterns](references/safe-arithmetic.md)
- [Initialization Patterns](references/initialization.md)
- [Event Emission Patterns](references/events.md)
- [Move V2 Syntax Patterns](references/v2-syntax.md)
- [Complete Example: NFT Collection](references/complete-example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Move code blocks and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask concise storage-design questions before recommending Aptos storage types.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
