## Description: <br>
Helps developers choose the appropriate Circle wallet type for onchain applications by comparing developer-controlled, user-controlled, and modular passkey wallets across custody, key management, account types, blockchain support, and implementation patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mscandlen3](https://clawhub.ai/user/mscandlen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to select a Circle wallet architecture before implementing blockchain wallet flows. It helps compare custody model, authentication method, account type, gas sponsorship, chain support, and when to delegate to a more specific wallet implementation skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet type selection affects custody, transaction authority, and potential financial exposure, especially for developer-controlled wallet flows. <br>
Mitigation: Use this as a decision aid, verify current Circle documentation, review any wallet-specific follow-up skill before implementation, and require deliberate review for developer-controlled flows. <br>


## Reference(s): <br>
- [Circle Wallet Account Types](https://developers.circle.com/wallets/account-types) <br>
- [Choosing Your Wallet Type](https://developers.circle.com/wallets/infrastructure-models) <br>
- [Circle Wallet Key Management](https://developers.circle.com/wallets/key-management) <br>
- [Circle Developer Docs](https://developers.circle.com/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with comparison tables and scenario-based recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to a wallet-specific follow-up skill; does not execute code or access credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
