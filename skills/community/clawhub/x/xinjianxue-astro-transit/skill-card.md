## Description:

心鉴学占星运势专业版：以本命盘为底，叠加当下行运星，解释这一段时间的议题、压力点与机会窗口。用户问「我最近运势」「今年事业/感情走向」「当下该注意什么」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide birth details and their current city to receive a paid astrology transit reading focused on current themes, pressures, and opportunities. The reading describes tendencies over time rather than certain events on specific dates.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Birth date, birth time, birthplace, and current city are sent to the service before the payment decision; retention and deletion terms are not provided.

Mitigation: Explain what information will be sent and obtain the user's consent before submitting it; do not promise retention or deletion practices that are not documented.

Risk: Each successful reading costs 6 CNY and requires separate Alipay authorization.

Mitigation: Disclose the price and authorization requirement before proceeding, and continue only with the user's consent.

## Reference(s):

- [API contract](references/api.md)
- [Reading framework](references/reading.md)
- [Payment flow](references/payment.md)
- [Astro Transit service API](https://api.xinjianxue.com/api/xinjianxue/aipay/astro-transit)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-astro-transit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown astrology reading]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Time-period-based interpretation framed as tendencies, not certain events on specific dates.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
