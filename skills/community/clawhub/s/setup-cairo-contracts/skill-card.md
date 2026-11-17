## Description:

Set up a Cairo smart contract project with OpenZeppelin Contracts for Cairo on Starknet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

AGPL-3.0-only

## Use Case:

Developers and engineers use this skill to scaffold Scarb/Starknet projects, add OpenZeppelin Contracts for Cairo dependencies, and apply Cairo import and component conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a shell command that runs a live remote installer without verification.

Mitigation: Use an official, pinned, and verifiable installation method, or download and verify the installer before running it.

Risk: Composed Cairo components can collide in flattened substorage and corrupt contract state.

Mitigation: Review the source of each composed component for internal storage variable naming conflicts before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/setup-cairo-contracts)
- [OpenZeppelin Contracts for Cairo documentation](https://docs.openzeppelin.com/contracts-cairo)
- [Starkup installer](https://sh.starkup.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, TOML, and Cairo code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, dependency snippets, import examples, and component composition guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
