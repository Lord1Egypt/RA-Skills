## Description:

心鉴学人性深度剖析专业版：用出生信息生成特征编码画像，按「判度＋双链条」解析亲密关系、职场、家庭中的具体困惑。用户问「他为什么这样对我」「怎么和领导/伴侣/父母相处」「这段关系要不要继续」「我到底是什么样的人」时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users seeking help with relationship, workplace, family, or self-understanding questions use this skill to receive a focused interpretation based on their birth details and a generated profile. It answers the user's specific question in concise Chinese guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends birth details, including date and time and birthplace, to an external provider before asking for payment.

Mitigation: Explain the external data transfer and obtain explicit user approval before making the request; check the provider's data-retention practices.

Risk: Each successfully delivered report costs 6 CNY.

Mitigation: Disclose the charge and obtain payment authorization; if payment is declined or not confirmed, stop without delivering the interpretation.

## Reference(s):

- [API contract](artifact/references/api.md)
- [Reading guidance](artifact/references/reading.md)
- [Payment flow](artifact/references/payment.md)
- [Analysis API endpoint](https://api.xinjianxue.com/api/xinjianxue/aipay/report)
- [ClawHub release page](https://clawhub.ai/weixin97676414/skills/xinjianxue-relation-advisor)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Concise Chinese Markdown response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 800 Chinese characters; addresses only the user's current question and avoids internal feature codes.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
