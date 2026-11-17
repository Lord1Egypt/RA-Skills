## Description:

心鉴学梅花易数专业版：用户随口报两个数即可起卦，得本卦、互卦、变卦、体用与卦辞，用于当下的一件事。用户说「梅花易数」「报数起卦」「我报两个数你算一下」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users can provide two positive integers and a brief question about a current situation to receive a Mei Hua Yi Shu reading and a concise, practical suggestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The numbers and optional question are sent to an external provider, and privacy or retention terms are not supplied.

Mitigation: Avoid names and confidential details in the question.

Risk: Each successfully delivered reading costs 6 CNY and requires a separate Alipay authorization.

Mitigation: Verify the merchant and amount before authorizing payment; do not proceed if payment is declined or unclear.

Risk: A divination reading could be mistaken for authoritative advice on a high-stakes matter.

Mitigation: Do not use readings for medical diagnosis, legal conclusions, investment decisions, or predictions about life and death.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-meihua)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [Service API contract](https://api.xinjianxue.com/api/xinjianxue/aipay/meihua)
- [Reading framework](artifact/references/reading.md)
- [Payment instructions](artifact/references/payment.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Concise Markdown reading with headings and emphasized key phrases]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 600 Chinese characters; includes the returned hexagram details and one current suggestion. Not for medical, legal, investment, or life-and-death decisions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
