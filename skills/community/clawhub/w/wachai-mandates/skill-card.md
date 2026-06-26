## Description: <br>
Create, sign, and verify WachAI Mandates, which are verifiable agent-to-agent agreements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Akshat-Mishra101](https://clawhub.ai/user/Akshat-Mishra101) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agents use this skill to create, sign, verify, store, and exchange WachAI Mandates for cryptographically verifiable agent-to-agent agreements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet material and mandate storage can expose private keys or sensitive agreement data if handled carelessly. <br>
Mitigation: Use a low-value or dedicated wallet, protect wallet.json with restrictive filesystem permissions, and keep WACHAI_STORAGE_DIR and WACHAI_WALLET_PATH in secure locations. <br>
Risk: Mandates exchanged or retained through XMTP and local storage may contain confidential business terms or regulated data. <br>
Mitigation: Do not include secrets, regulated data, or confidential business terms unless the user accepts the XMTP transport and local retention model. <br>
Risk: Installing the global npm package executes third-party CLI code in the user's environment. <br>
Mitigation: Review the npm package or source before installation and use an isolated environment for evaluation. <br>


## Reference(s): <br>
- [WachAI Terminal](https://github.com/quillai-network/WachAI-Terminal) <br>
- [ClawHub skill page](https://clawhub.ai/Akshat-Mishra101/wachai-mandates) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local wallet and mandate files through the WachAI CLI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
