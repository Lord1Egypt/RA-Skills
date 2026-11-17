## Description:

Guides agents through upgrading Solidity smart contracts with OpenZeppelin proxy patterns, including UUPS, Transparent, and Beacon workflows, initializer practices, storage-layout safety, and Hardhat or Foundry upgrade validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-contract engineers use this skill to plan and implement upgradeable Solidity contracts with OpenZeppelin proxy patterns, validate storage-layout and initializer safety, and choose Hardhat or Foundry upgrade workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installs and Foundry ffi workflows can execute project or package code in the developer environment.

Mitigation: Install only in a trusted development environment, pin dependency versions or commits, and review lockfiles before running generated commands.

Risk: Deployment or upgrade guidance may affect live contracts or expose wallet keys, RPC credentials, or upgrade authority.

Mitigation: Do not run deployments or upgrades against production networks unless explicitly approved; use testnets or local forks and protect privileged credentials.

Risk: Incorrect storage-layout or initializer changes can corrupt proxy state or leave upgradeable implementations unsafe.

Mitigation: Run OpenZeppelin upgrade validation, review storage layout changes, and test the full upgrade path before executing on-chain upgrades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/upgrade-solidity-contracts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Solidity, JavaScript, TOML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
