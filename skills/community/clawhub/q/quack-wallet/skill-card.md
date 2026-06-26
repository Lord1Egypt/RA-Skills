## Description: <br>
Check balances and transfer Quack tokens through the Quack Network API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JPaulGrayson](https://clawhub.ai/user/JPaulGrayson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to check Quack token balances and send Quack Network token transfers for payments or agent fund management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token transfers can be sent with a stored Quack API key without built-in confirmation or transfer limits. <br>
Mitigation: Use a limited-scope or low-balance key when possible, and manually verify the recipient, amount, memo, and agent ID before running a transfer. <br>
Risk: The local Quack API key grants access to wallet balance and transfer actions. <br>
Mitigation: Store the credential only in the expected local credentials file and avoid using a key tied to balances you are not willing to expose to automated actions. <br>


## Reference(s): <br>
- [Quack Wallet on ClawHub](https://clawhub.ai/JPaulGrayson/quack-wallet) <br>
- [Quack Network API](https://quack.us.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON responses from the Quack Network API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Quack API key credential and command-line parameters for recipient, amount, memo, and optional agent ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
