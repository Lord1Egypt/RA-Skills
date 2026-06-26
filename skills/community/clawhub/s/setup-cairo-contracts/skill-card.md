## Description: <br>
Set up a Cairo smart contract project with OpenZeppelin Contracts for Cairo on Starknet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold Cairo and Starknet projects, add OpenZeppelin Contracts for Cairo dependencies, and apply the correct import and component patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow pipes a remote installer script into a shell. <br>
Mitigation: Verify https://sh.starkup.sh against official Starknet/Cairo documentation and inspect or download the installer before execution. <br>
Risk: Setup commands may be run in environments that also contain sensitive wallet or deployer credentials. <br>
Mitigation: Run the setup in a development environment and keep production wallet and deployer keys out of the session. <br>
Risk: Composing Cairo components with flattened substorage can cause storage slot conflicts. <br>
Mitigation: Review the source of each component being composed and confirm internal storage names do not conflict. <br>


## Reference(s): <br>
- [OpenZeppelin Contracts for Cairo documentation](https://docs.openzeppelin.com/contracts-cairo) <br>
- [Starkup installer](https://sh.starkup.sh) <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/setup-cairo-contracts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, TOML, and Cairo code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup commands, dependency snippets, import examples, and component composition guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
