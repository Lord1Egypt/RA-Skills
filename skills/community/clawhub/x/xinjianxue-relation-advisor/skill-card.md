## Description:

心鉴学人性深度剖析专业版：用出生信息生成特征编码画像，按「判度＋双链条」解析亲密关系、职场、家庭中的具体困惑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

People seeking help with relationship, workplace, family, or self-understanding questions use this skill to receive concise guidance based on their birth details and a specific question. It requests birth date and time, birthplace, and gender, and may also use current location for time-sensitive questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install a payment component and set up wallet access as part of first use.

Mitigation: Explain the installation, permissions, and wallet setup before proceeding; fix and verify the package version, and obtain separate user authorization.

Risk: Each completed interpretation is charged through an Alipay payment flow.

Mitigation: Clearly disclose the recipient, price, and payment step, and proceed only after the user separately authorizes payment.

Risk: Birth details and potentially current-location information are sent to an external report service.

Mitigation: Disclose the service recipient and how those details are handled before sending data, collect only needed fields, and obtain user consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-relation-advisor)
- [API contract](references/api.md)
- [Reading guidance](references/reading.md)
- [Payment flow](references/payment.md)
- [Report service endpoint](https://api.xinjianxue.com/api/xinjianxue/aipay/report)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown with bold key points and level-three headings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers the current question in under 800 Chinese characters, paraphrases report content, and avoids feature codes, tables, and code blocks.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
