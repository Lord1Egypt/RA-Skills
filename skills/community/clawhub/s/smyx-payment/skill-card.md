## Description: <br>
Provides LifeEmergence skill account recharge and renewal flows, balance and usage queries, balance checks, Alipay payment integration, and payment-page generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to review recharge packages, create skill account recharge or renewal orders, pay through Alipay, and check account balance or usage counts. It is intended for payment and account-service workflows tied to LifeEmergence skill accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates real Alipay payment orders and contacts LifeEmergence services. <br>
Mitigation: Install only when the publisher is trusted, review the payment flow before deployment, and require explicit permission documentation for payment actions. <br>
Risk: The skill handles account state and locally stored credentials or account stubs. <br>
Mitigation: Require no plaintext API key output, review local credential handling, and limit deployment to environments with appropriate credential controls. <br>
Risk: The security review calls out sensitive payment, account, and credential handling that is under-scoped for approval without review. <br>
Mitigation: Before production use, require verified Alipay server-side callbacks, real authentication for token issuance, and removal of mock or demo payment paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-payment) <br>
- [Alipay integration guide](artifact/references/alipay-integration-guide.md) <br>
- [Alipay merchant configuration](artifact/references/alipay-merchant-config.md) <br>
- [API configuration reference](artifact/references/api-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation output with payment QR image references, account status fields, and inline shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Payment URLs should not be shown to users; outputs may include package options, QR payment cards, account identifiers, and balance or usage summaries.] <br>

## Skill Version(s): <br>
1.0.23 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
