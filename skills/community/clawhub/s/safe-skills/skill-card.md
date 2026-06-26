## Description: <br>
Safe Skills helps agents create and manage EVM wallets, check balances, transfer tokens, and send transactions without exposing raw private keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glitch003](https://clawhub.ai/user/glitch003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to delegate EVM wallet operations to an agent while keeping wallet keys server-side. It supports wallet creation, balance checks, token transfers, and contract transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent persistent authority to move crypto funds and send arbitrary blockchain transactions. <br>
Mitigation: Use testnet or small amounts first, require explicit confirmation for every transfer or smart-contract transaction, and set strict spending policies when available. <br>
Risk: The wallet API key can authorize future wallet operations if exposed in chat, logs, or shared files. <br>
Mitigation: Store the API key outside chat and logs, pass it only as a Bearer token when needed, and rotate or revoke access if exposure is suspected. <br>
Risk: Blockchain transfers and custom calldata transactions can be irreversible or interact with unintended contracts. <br>
Mitigation: Verify chain, recipient, token contract, amount, calldata, provider identity, and claim URL controls before funding a wallet or approving a transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/glitch003/safe-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Bearer API key returned during wallet creation; claim URLs should be shared with the user for policy management and activity monitoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
