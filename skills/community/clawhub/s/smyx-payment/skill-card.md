## Description: <br>
Provides skill-account recharge and renewal workflows, balance and usage-count queries, balance checks, Alipay payment integration, and payment-page generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to choose a skill-account package, generate an Alipay payment page, and later query account balance or remaining usage when they explicitly request it. Developers and operators should review the bundled payment, identity, callback, and demo utilities before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist local account or API-key state and interact with external payment and account services. <br>
Mitigation: Install only for trusted publishers, review configuration and local state behavior before use, and restrict credentials to the minimum required environment. <br>
Risk: Payment-success callback, mock payment, demo, admin, and monitoring scripts are bundled with the release. <br>
Mitigation: Treat those auxiliary scripts as non-production until backend verification, permissions, and user-confirmation boundaries are reviewed. <br>
Risk: Payment handling depends on cloud order creation, Alipay payment pages, private-key handling, and manual balance-query boundaries. <br>
Mitigation: Require cloud-returned order numbers, keep private keys in process memory only, avoid automatic balance or order-status checks after page generation, and query balances only on explicit user request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-payment) <br>
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui) <br>
- [Alipay integration guide](artifact/references/alipay-integration-guide.md) <br>
- [API configuration reference](artifact/references/api-config.md) <br>
- [Token schemes reference](artifact/references/token-schemes.md) <br>
- [Alipay developer platform](https://open.alipay.com/) <br>
- [Life Emergence service endpoint](https://lifeemergence.com/jeecg-boot-xzgz) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown payment instructions, shell-command entrypoints, generated payment links or QR-code pages, and account-balance tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact external payment and account services and may persist local account or API-key state.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
