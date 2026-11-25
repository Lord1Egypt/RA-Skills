## Description:

Provides a paid Chinese Bazi reading from a person's birth date, time, gender, and birthplace, covering the Four Pillars, five-element balance, major luck cycles, and annual trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide their birth date and time, gender, and birthplace to request a Four Pillars chart, five-element reading, major luck-cycle overview, and annual trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious because it combines birth-chart services with payment-wallet operations, automatic payment-software installation, and external transmission of personal birth details; the scan is partial.

Mitigation: Do not install until the payment and wallet steps are removed or clearly explained and separately approved; verify the package source and exact version. Check what birth details are sent to the external service and how they are handled.

Risk: Each successful chart costs 6 CNY and uses an Alipay AI Pay payment flow that requires buyer-side payment setup.

Mitigation: Review and separately approve payment setup and each charge before requesting a chart.

Risk: Birth date, time, gender, and birthplace are sent to an external chart service.

Mitigation: Before sharing birth details, check what is sent and how the service handles it.

## Reference(s):

- [Reading framework](references/reading.md)
- [Payment details](references/payment.md)
- [API contract](references/api.md)
- [Bazi chart service](https://api.xinjianxue.com/api/xinjianxue/aipay/bazi)
- [ClawHub release page](https://clawhub.ai/weixin97676414/skills/xinjianxue-diag-2042)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with headings and bold key points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized reading based on returned chart data; the skill specifies no tables.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
