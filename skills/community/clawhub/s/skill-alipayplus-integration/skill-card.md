## Description: <br>
Helps acquirers and mobile payment providers integrate Alipay+ payments, generate configuration, test signatures, debug ACQP notifications, and process reconciliation files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wypride](https://clawhub.ai/user/wypride) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and payment-integration engineers use this skill to plan ACQP or MPP Alipay+ integrations, prepare sandbox or production configuration, test RSA2 signatures, debug ACQP webhook notifications, and reconcile settlement files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles payment credentials, private keys, webhook payloads, and transaction or settlement data. <br>
Mitigation: Use sandbox credentials first, avoid pasting production secrets into prompts or logs, and restrict permissions on generated key, configuration, notification, and reconciliation files. <br>
Risk: Webhook debugging can log complete notification requests and may expose a local service through ngrok. <br>
Mitigation: Use only non-production payloads for debugging, avoid ngrok for production traffic, and delete notification logs after testing. <br>
Risk: Reconciliation helpers download and process payment settlement files that can contain sensitive transaction data. <br>
Mitigation: Store reports in a controlled workspace, clean up CSV and text reports after review, and share only redacted discrepancy summaries. <br>
Risk: Security evidence calls out SFTP host-key and signature-example issues before copying examples into production. <br>
Mitigation: Review scripts before execution, pin and verify SFTP host keys, and validate signature examples against current official Alipay+ documentation before production use. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/wypride/skill-alipayplus-integration) <br>
- [Alipay+ ACQP API Overview](https://docs.alipayplus.com/alipayplus/alipayplus/api_acq_tile/) <br>
- [Alipay+ MPP API Overview](https://docs.alipayplus.com/alipayplus/alipayplus/api_mpp/) <br>
- [Alipay+ ACQP Customer-Presented Mode](https://docs.alipayplus.com/alipayplus/alipayplus/integration_user_mode_acq/accept_payment) <br>
- [Alipay+ ACQP Merchant-Presented Order Code](https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_acq/accept_payment_order_code) <br>
- [Alipay+ ACQP Merchant-Presented Entry Code](https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_acq/accept_payment_entry_code) <br>
- [Alipay+ MPP Customer-Presented Mode](https://docs.alipayplus.com/alipayplus/alipayplus/integration_user_mode_mpp/accept_payments) <br>
- [Alipay+ MPP Merchant-Presented Mode](https://docs.alipayplus.com/alipayplus/alipayplus/integration_merchant_mode_mpp/accept_payments) <br>
- [API Reference](references/api-reference.md) <br>
- [Integration Flows](references/flows.md) <br>
- [Signature Guide](references/signature-guide.md) <br>
- [Webhook Guide](references/webhook-guide.md) <br>
- [Reconciliation Guide](references/reconciliation-guide.md) <br>
- [Configuration Template](references/config-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration, key, notification log, reconciliation CSV, and reconciliation report files under the user's workspace when helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
