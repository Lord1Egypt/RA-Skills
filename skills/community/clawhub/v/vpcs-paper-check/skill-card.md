## Description:

帮助用户选择维普 VPCS 检测产品、核对价格与订单，并指导文档上传、报告下载和官方验真。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zslzxy](https://clawhub.ai/user/zslzxy)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要中文论文检测的用户，帮助选择 15 种 VPCS 产品，了解价格与订单流程，并在用户确认后上传文档、查询报告及前往官方页面验真。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitting an order may upload a private document to the VPCS/OSS workflow.

Mitigation: Confirm the exact product, selected file and user consent before submission.

Risk: Stale prices or different institutional rules could mislead purchasing decisions.

Mitigation: Check final prices on the live site and acceptance requirements with the institution.

Risk: Automating payment or report verification could bypass user-controlled steps.

Mitigation: Leave payment, CAPTCHA and official report verification to the user in the browser.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zslzxy/skills/vpcs-paper-check)
- [VPCS product and pricing FAQ](https://vpcs.cqccjy.cn/faq/vip/8)
- [VPCS report verification](https://vpcs.cqccjy.cn/pwp/verify)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product selection, order and report guidance; verification and payment remain in the browser.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
