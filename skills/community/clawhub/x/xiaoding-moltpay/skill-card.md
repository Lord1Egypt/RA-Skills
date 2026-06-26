## Description: <br>
AI Agent's crypto wallet manager - generate wallets, manage transactions, and claim ORA token rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use MoltsPay to generate local BTC, ETH, and SOL wallet credentials, register public wallet addresses with MoltPay, track ORA balance and transaction history, and request withdrawals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill asks an agent to handle real wallet secrets and financial flows with weak safeguards. <br>
Mitigation: Do not use with real funds unless the user has reviewed the flow; prefer an audited wallet or encrypted key store and require explicit human approval for registration, withdrawal, transaction recording, and funding requests. <br>
Risk: The artifact stores generated private keys and mnemonics in a local wallets.json file. <br>
Mitigation: Store wallet secrets only in an encrypted keystore or hardware-backed wallet, restrict file permissions, and avoid retaining plaintext mnemonics in agent-accessible files. <br>
Risk: The security guidance notes external sharing of wallet and transaction data. <br>
Mitigation: Share only intended public addresses and transaction metadata, review the destination services before use, and avoid sending private keys, mnemonics, or unnecessary personal information. <br>
Risk: The artifact includes recurring network checks and prompts to display wallet QR codes to request funding. <br>
Mitigation: Disable or tightly scope heartbeat checks, inspect responses before acting on them, and require explicit user approval before displaying QR codes or asking a human to send crypto. <br>


## Reference(s): <br>
- [MoltsPay ClawHub listing](https://clawhub.ai/asterisk622/xiaoding-moltpay) <br>
- [MoltPay service](https://moltpay.net) <br>
- [Publisher profile](https://clawhub.ai/user/asterisk622) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with Python, bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet setup guidance, local file paths, QR code display steps, and API endpoint examples.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
