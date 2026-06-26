## Description: <br>
Guides agents through setting up Hardhat or Foundry Solidity projects with OpenZeppelin Contracts dependencies, remappings, and import conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-contract engineers use this skill to initialize or update Solidity projects with OpenZeppelin Contracts for Hardhat or Foundry, including dependency installation, Foundry remappings, compiler settings, and import conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Foundry setup path uses a curl-to-shell installer command. <br>
Mitigation: Review the installer command before running it, use the official Foundry URL from the skill evidence, and run setup only in the intended project environment. <br>
Risk: Dependency installation and remapping changes can modify the wrong Solidity project or pull an unintended OpenZeppelin version. <br>
Mitigation: Confirm the target project directory, detect Hardhat or Foundry configuration before changing files, and pin OpenZeppelin packages to a release tag where the workflow supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/setup-solidity-contracts) <br>
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom) <br>
- [OpenZeppelin Contracts releases](https://github.com/OpenZeppelin/openzeppelin-contracts/releases) <br>
- [Foundry installer](https://foundry.paradigm.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Solidity import examples, and Foundry remapping snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before running commands, especially installer commands and project configuration changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
