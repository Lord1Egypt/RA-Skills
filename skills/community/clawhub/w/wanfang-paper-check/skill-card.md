## Description:

指导用户选择万方检测产品、上传论文、创建和查询订单，并获取、解读及验真报告；付款和验证码填写由用户自行完成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zslzxy](https://clawhub.ai/user/zslzxy)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要论文查重或文本 AIGC 检测的用户，协助选择合适产品、提交文档、跟踪原订单，并查看与验真报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A selected paper is uploaded to the CQCCJY WanFang service.

Mitigation: Upload only a document you intend to submit to that service; review its contents before confirming.

Risk: Product choice or price may differ from an older snapshot.

Mitigation: Check the live product and price before submitting; complete payment and any captcha yourself in the browser.

Risk: A report or successful verification may be mistaken for institutional acceptance.

Mitigation: Interpret only fields shown in the report and follow the relevant school or journal's written requirements.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zslzxy/skills/wanfang-paper-check)
- [万方公共用户端](https://wanfang.cqccjy.cn/pwf)
- [报告验真入口](https://vpcs.cqccjy.cn/pwp/verify)
- [万方官方验真备用页](https://truth.wanfangdata.com.cn/)
- [万方公共工作流](artifact/references/workflow.md)
- [报告下载、阅读与验真](artifact/references/report-and-verification.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Chinese-language guidance and structured order/status results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product choices, order status, report links and browser handoff URLs; payment remains user-controlled.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
