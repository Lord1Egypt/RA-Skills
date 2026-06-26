## Description: <br>
ZL-ClawPay helps agents bind a sub-wallet, submit explicit payment requests, query payment status, and retrieve transaction records through a Node.js CLI using SM2/SM3/SM4 encrypted communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevindagege](https://clawhub.ai/user/kevindagege) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and payment-enabled agents use this skill to manage a ZL-ClawPay sub-wallet, initiate user-confirmed payments, check order status, and review transaction records. It is intended for explicit payment and wallet workflows, not general finance, balance inquiry, batch export, or QR-code collection scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit live payment requests using stored payment credentials. <br>
Mitigation: Require explicit confirmation for each transaction, including merchant, amount, and order details, before executing payment commands. <br>
Risk: Stored API keys and wallet identifiers create exposure if local credential storage is compromised. <br>
Mitigation: Protect credentials in an appropriate secret store or hardened local environment and restrict access to ~/.zl-claw-pay/state.json. <br>
Risk: Unbind or revocation commands can be destructive and may permanently disable an API key. <br>
Mitigation: Treat unbind and revocation flows as high-impact operations and require clear user confirmation before execution. <br>
Risk: Plaintext response fallback in production can weaken confidentiality expectations for payment responses. <br>
Mitigation: Disable plaintext response fallback before production use and rely on encrypted payment API responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kevindagege/zl-clawpay) <br>
- [API Specification](references/api-spec.md) <br>
- [Credential Setup Guide](references/credential-setup-guide.md) <br>
- [Request Examples](assets/request-examples.md) <br>
- [Dependency Guide](references/dependency-guide.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local credential storage and outbound HTTPS payment API calls when the agent executes the documented CLI commands.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
