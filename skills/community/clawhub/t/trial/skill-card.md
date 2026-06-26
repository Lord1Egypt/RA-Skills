## Description: <br>
Send and receive KAS cryptocurrency. Check balances, send payments, generate wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Manyfestation](https://clawhub.ai/user/Manyfestation) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to operate a Kaspa command-line wallet: install the Python dependency, configure wallet credentials, check balances and network status, estimate fees, generate payment URIs or mnemonics, and send KAS transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use wallet secrets to send funds immediately. <br>
Mitigation: Review carefully before installation, start on testnet or with a low-balance wallet, and require explicit human confirmation before any send, max, or consolidation command. <br>
Risk: Private keys or mnemonics are supplied through environment variables that may be exposed in shared shells or agent sessions. <br>
Mitigation: Avoid using production wallet secrets in shared environments and clear sensitive environment variables after use. <br>
Risk: The kaspa dependency is declared without a pinned version. <br>
Mitigation: Review or pin the kaspa package version before use in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Manyfestation/trial) <br>
- [Publisher profile](https://clawhub.ai/user/Manyfestation) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/README.md](artifact/README.md) <br>
- [Kaspa Python package](https://pypi.org/project/kaspa/) <br>
- [Kaspa mainnet explorer](https://explorer.kaspa.org/) <br>
- [Kaspa testnet explorer](https://explorer-tn10.kaspa.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return structured JSON and use environment variables for wallet secrets, network selection, RPC URL, and timeout settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
