## Description:

心鉴学八字命理专业版：出生年月日时分＋性别＋出生地 → 四柱、五行强弱、起运、十步大运与流年。用户要求排八字、批命、算命、看大运流年、问五行缺什么、喜用神、日主强弱、今年运势时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

People seeking a BaZi reading use the skill to request a four-pillars chart, five-element balance, favorable-element guidance, and discussion of life-cycle or annual trends. The skill requests the required birth details and grounds its reading in the chart service response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the chart service sends the user's birth date, time, sex, and birthplace to api.xinjianxue.com; retention practices are unspecified.

Mitigation: Explain the data sharing before submitting details and proceed only with the user's informed consent.

Risk: A delivered chart costs ¥6, and payment details require user review.

Mitigation: Clearly disclose the fee, obtain approval before payment, and use the separate payment capability obtained through Alipay's official channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-bazi)
- [API contract](references/api.md)
- [Payment instructions](references/payment.md)
- [Reading framework](references/reading.md)
- [Chart service endpoint](https://api.xinjianxue.com/api/xinjianxue/aipay/bazi)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Chinese natural-language birth-chart interpretation with Markdown headings and emphasis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chart details are based on the service response; interpretations use non-deterministic language and avoid medical, legal, and investment predictions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
