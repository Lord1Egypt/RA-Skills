## Description:

心鉴学八字命理专业版：出生年月日时分＋性别＋出生地 → 四柱、五行强弱、起运、十步大运与流年。用户要求排八字、批命、算命、看大运流年、问五行缺什么、喜用神、日主强弱、今年运势时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide birth date, time, gender, and birthplace to request a BaZi chart and a reading of its five-element balance, major cycles, and annual trends. The skill returns an interpretation organized around the user's question.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth date, time, gender, and birthplace are sent to an external service, and the scanner reports no privacy notice.

Mitigation: Before submitting those details, check for clear disclosure of what is sent, who receives it, and how it is handled; share only details you are comfortable providing.

Risk: The skill directs local installation of a third-party payment package and setup of payment-wallet permissions.

Mitigation: Proceed only if you are comfortable with the installation and payment setup; review the package and wallet permissions and know how to revoke them.

## Reference(s):

- [API contract](artifact/references/api.md)
- [Payment flow](artifact/references/payment.md)
- [Reading framework](artifact/references/reading.md)
- [BaZi service endpoint](https://api.xinjianxue.com/api/xinjianxue/aipay/bazi)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-bazi)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Markdown interpretation based on chart data returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only fields present in the service response; frames readings as tendencies and avoids medical diagnosis, legal outcomes, and investment predictions.]

## Skill Version(s):

2.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
