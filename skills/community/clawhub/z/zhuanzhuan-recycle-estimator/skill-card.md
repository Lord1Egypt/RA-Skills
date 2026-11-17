## Description:

Zhuanzhuan Recycle Estimator helps an agent identify pre-owned goods from text or images and return a reference trade-in price with follow-up questions when key details are missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjinxinlove](https://clawhub.ai/user/chenjinxinlove)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to estimate recycle values for phones, tablets, laptops, electronics, and small appliances before deciding whether to proceed through Zhuanzhuan Recycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Valuation text and product photos are sent to the Zhuanzhuan service.

Mitigation: Use the skill only when users consent to sharing product descriptions or photos, and avoid uploading arbitrary local files.

Risk: Caller-controlled base URLs could route data or responses through an untrusted endpoint.

Mitigation: Do not use --base-url except with a trusted approved endpoint.

Risk: Remote reply text can influence final agent responses.

Mitigation: Treat service-generated reply text as untrusted when maintaining or wrapping this skill, and review outputs before surfacing them in higher-risk workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjinxinlove/skills/zhuanzhuan-recycle-estimator)
- [Publisher profile](https://clawhub.ai/user/chenjinxinlove)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text responses with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include follow-up questions, structured choices, and reference valuation ranges; estimates are not binding offers.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
