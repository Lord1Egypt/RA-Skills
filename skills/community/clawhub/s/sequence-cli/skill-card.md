## Description: <br>
Manage Sequence smart wallets, projects, API keys, ERC20 transfers, and query blockchain data using the Sequence Builder CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesLawton](https://clawhub.ai/user/JamesLawton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate the Sequence Builder CLI for wallet creation, login, project and API key management, ERC20 transfers, and blockchain data queries across supported EVM networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to create wallets, use private keys, and submit ERC20 transfers. <br>
Mitigation: Use testnets or minimal funds first and require explicit human confirmation of recipient, token contract, amount, and chain before any transfer. <br>
Risk: Private keys, encrypted wallet configuration, and SEQUENCE_PASSPHRASE can expose wallet control if mishandled. <br>
Mitigation: Avoid passing private keys directly in chat or command lines where possible and protect ~/.sequence-builder/config.json and SEQUENCE_PASSPHRASE. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JamesLawton/sequence-cli) <br>
- [Sequence Builder CLI Repository](https://github.com/0xsequence/builder-cli) <br>
- [Sequence Network Status](https://status.sequence.info/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended to use --json when results are parsed programmatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
