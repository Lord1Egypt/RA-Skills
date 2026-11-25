## Description:

心鉴学八字命理专业版：出生年月日时分＋性别＋出生地 → 四柱、五行强弱、起运、十步大运与流年。用户要求排八字、批命、算命、看大运流年、问五行缺什么、喜用神、日主强弱、今年运势时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users use the skill to request a BaZi chart and a structured reading of its five elements, major cycles, and annual trends based on birth details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags payment-wallet actions and payment software setup in the workflow as suspicious.

Mitigation: Review the package source and version, and explain and separately authorize payment-related steps before proceeding.

Risk: The workflow sends personal birth details to an external service, and the security review notes there is no privacy disclosure.

Mitigation: Clarify how the external service handles birth details and let the user decide whether to share them.

## Reference(s):

- [API contract](artifact/references/api.md)
- [Payment flow](artifact/references/payment.md)
- [Reading framework](artifact/references/reading.md)
- [BaZi service endpoint](https://api.xinjianxue.com/api/xinjianxue/aipay/bazi)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-diag-t2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prose with headings and highlighted key points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A structured reading based only on the chart data returned by the service.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
