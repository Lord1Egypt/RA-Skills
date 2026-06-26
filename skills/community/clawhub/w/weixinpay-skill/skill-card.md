## Description: <br>
Guides agents through WeChat Pay merchant onboarding, payment API integration, QR-code collection, refunds, bill reconciliation, and credential handling for scan-to-pay workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piaoleaf](https://clawhub.ai/user/piaoleaf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators use this skill to plan and explain WeChat Pay integrations, including merchant setup, Native QR-code payment flows, callbacks, refunds, bill downloads, and marketing payout workflows. Ordinary payment users provide non-secret order and merchant identifiers, while administrators manage the required WeChat Pay credentials outside chat. <br>

### Deployment Geography for Use: <br>
China, subject to WeChat Pay merchant eligibility and applicable payment rules. <br>

## Known Risks and Mitigations: <br>
Risk: WeChat Pay credentials, merchant private keys, signing keys, API keys, and platform certificates could be exposed or mishandled during deployment. <br>
Mitigation: Store credentials outside chat in a protected secrets manager or equivalent, restrict access to administrators, rotate credentials regularly, avoid logging secrets, and load credentials only for authorized payment operations. <br>
Risk: Refunds, bill downloads, red-packet, and marketing payout workflows can move funds or expose financial records if used without authorization. <br>
Mitigation: Require explicit authorization, role-based access control, and audit logging before executing sensitive payment or reporting actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/piaoleaf/weixinpay-skill) <br>
- [Publisher profile](https://clawhub.ai/user/piaoleaf) <br>
- [WeChat Pay merchant platform](https://pay.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with process steps, operational checklists, and integration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Payment actions depend on administrator-managed WeChat Pay credentials; secrets should stay outside chat and protected storage, and refunds, bill downloads, red-packet, or marketing payout actions should require explicit authorization and audit logging.] <br>

## Skill Version(s): <br>
1.0.7 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
