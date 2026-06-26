## Description: <br>
Walletconnect Agent lets an AI agent connect to Web3 dApps through WalletConnect v2 and sign messages or blockchain transactions from a configured wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daaab](https://clawhub.ai/user/daaab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Web3 operators use this skill to let an agent connect to WalletConnect-compatible dApps, submit actions such as swaps, mints, votes, or Base name registration, and optionally prompt before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent sign real blockchain messages and transactions with broad wallet authority. <br>
Mitigation: Use only a dedicated low-value wallet, keep balances small, and add external safeguards such as contract allowlists, spend limits, and transaction simulation. <br>
Risk: Auto-approval can sign requests from malicious or unexpected dApps. <br>
Mitigation: Use interactive mode for new dApps, connect only to trusted dApps, and review audit logs after use. <br>
Risk: The workflow requires a private key and can expose funds if the key is reused or mishandled. <br>
Mitigation: Do not use a main wallet or reusable private key; provide keys only through environment variables and rotate or discard wallets after high-risk use. <br>
Risk: Raw eth_sign support can enable arbitrary-data signing if explicitly enabled. <br>
Mitigation: Keep eth_sign blocked unless a specific trusted workflow requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daaab/walletconnect-agent) <br>
- [Base Names](https://www.base.org/names) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce command lines that use wallet private keys through environment variables and may trigger real blockchain signing workflows.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release evidence; artifact package.json and _meta.json report 1.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
