## Description:

Set up a Solidity smart contract project with OpenZeppelin Contracts for Hardhat or Foundry projects, including dependencies, Foundry remappings, and Solidity import conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to bootstrap Solidity smart contract projects with OpenZeppelin Contracts, choose Hardhat or Foundry setup steps, and configure dependency imports and remappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing Foundry with a mutable remote script piped directly into Bash.

Mitigation: Inspect the installer before execution or use a pinned, verified Foundry release instead of executing curl output directly.

Risk: Solidity dependency and compiler setup guidance can affect deployed contract behavior if versions or EVM settings are mismatched.

Mitigation: Pin OpenZeppelin dependencies to release tags and confirm the Solidity compiler and EVM version match the intended deployment chain.

## Reference(s):

- [OpenZeppelin Contracts releases](https://github.com/OpenZeppelin/openzeppelin-contracts/releases)
- [Foundry installer](https://foundry.paradigm.xyz)
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/setup-solidity-contracts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup guidance and commands; users should review commands before execution.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
