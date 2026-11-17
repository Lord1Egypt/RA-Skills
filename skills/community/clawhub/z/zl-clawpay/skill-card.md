## Description: <br>
ZL-ClawPay lets an agent bind a sub-wallet, initiate passwordless payments, and query payment status or transaction records through a Node.js CLI using SM2/SM3/SM4 encrypted communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevindagege](https://clawhub.ai/user/kevindagege) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to connect a ZLPay sub-wallet, perform explicit payment requests, and inspect payment status or transaction records. It is intended for payment workflows where the user has provided credentials and confirms the merchant, amount, order details, and transaction identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real payments through an agent after local wallet credentials are configured. <br>
Mitigation: Require explicit user intent and display the merchant, amount, order details, and seqId before every payment. <br>
Risk: Payment credentials are stored locally and may expose financial authority if the local environment is compromised. <br>
Mitigation: Use the skill only on trusted machines, confirm wallet payment limits in the wallet app, and revoke or clear bindings when access is no longer needed. <br>
Risk: Credential-storage documentation may be misleading or incomplete for users assessing security. <br>
Mitigation: Review the credential setup guide and security summary before installation, and avoid entering credentials unless the storage behavior is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kevindagege/zl-clawpay) <br>
- [Publisher profile](https://clawhub.ai/user/kevindagege) <br>
- [API specification](references/api-spec.md) <br>
- [Credential setup guide](references/credential-setup-guide.md) <br>
- [Dependency guide](references/dependency-guide.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Request examples](assets/request-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include payment status, transaction records, wallet binding state, and user-facing confirmation text.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
