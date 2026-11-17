## Description:

八字命理解读，1500000字个人命理报告。用户询问个人运势、性格、事业、财运、婚姻、健康倾向、某年某月发生什么时使用；负责获取服务端结构化命理报告，并按心鉴学规则给出解读。包含账号注册、可用次数查询、报告下载与论断边界。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

For users seeking a BaZi reading, the skill retrieves a structured report using birth details and explains personality and life-area tendencies or themes for a selected year or month. It frames readings as tendencies and does not provide medical, legal, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends precise birth details to a remote service without a required warning.

Mitigation: Tell the user before sending birth details to the remote service and proceed only with their agreement; do not submit another person's birth details without consent.

Risk: A server-controlled report filename could cause JSON output to be written outside the chosen directory.

Mitigation: Use a dedicated, unprivileged report directory and confirm the resolved output path stays within it before saving.

Risk: The security scan was partial because two local path-like references were unresolved.

Mitigation: Resolve the missing references and review the skill again before relying on the incomplete scan.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/weixin97676414/skills/xix-bazi)
- [神煞内容参考表](references/1-神煞内容参考表.md)
- [原命局宫位取像表](references/2-原命局宫位取像表.md)
- [十神取象表](references/3-十神取象表.md)
- [心鉴学人性分析规则](references/4-心鉴学人性分析规则.md)
- [喜用神与吉凶判断规则](references/5-喜用神与吉凶判断规则.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON files]

**Output Format:** [Markdown explanations and a downloaded JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The large structured report is saved to disk; answers address the current question and describe tendencies rather than certainties.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
