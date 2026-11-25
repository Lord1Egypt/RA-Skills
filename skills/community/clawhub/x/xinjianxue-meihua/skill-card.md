## Description:

心鉴学梅花易数专业版：用户随口报两个数即可起卦，得本卦、互卦、变卦、体用与卦辞，用于当下的一件事。用户说「梅花易数」「报数起卦」「我报两个数你算一下」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide two numbers and an optional question to receive a Meihua Yishu reading for a current situation, followed by a practical suggestion. The skill excludes medical, legal, investment, and life-or-death questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes Alipay wallet setup and a ¥6 charge for each successfully delivered reading.

Mitigation: Explain the fee and payment steps, and obtain the user's consent before wallet setup or payment.

Risk: Initial setup installs unpinned payment software and the reading uses an external API.

Mitigation: Review the installation commands and external payment workflow; proceed only when the user is comfortable with them.

## Reference(s):

- [API contract](references/api.md)
- [Alipay payment flow](references/payment.md)
- [Reading framework](references/reading.md)
- [Meihua Yishu service endpoint](https://api.xinjianxue.com/api/xinjianxue/aipay/meihua)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One reading of up to 600 Chinese characters, with a present-focused interpretation and practical suggestion.]

## Skill Version(s):

2.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
