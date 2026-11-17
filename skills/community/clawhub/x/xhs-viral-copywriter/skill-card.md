## Description:

爆款文案助手适合内容创作者、运营、市场营销、内容媒体在用户提出“小红书怎么写才有人看”这类问题，需要快速拆解目标、判断重点并形成可执行结果时使用，帮助基于输入材料生成摘要、诊断结论、行动建议和可复用交付物。

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operations teams, marketers, and media teams use this skill to turn a Xiaohongshu topic, audience, tone, note type, selling point, and account persona into copywriting summaries, diagnostic conclusions, action suggestions, and reusable deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided topics, audience details, selling points, account persona, and enabled profile context are sent to the AI Skills service.

Mitigation: Use only a trusted HTTPS AISKILLS_BASE_URL and avoid submitting secrets, unpublished confidential plans, regulated personal data, or other sensitive material.

Risk: The runner requires AISKILLS_API_KEY for authentication.

Mitigation: Keep the API key private, provide it through environment variables, and do not paste it into prompts, logs, or shared configuration.

Risk: Generated copywriting guidance may be incomplete, inaccurate, or unsuitable for a brand or regulated claim.

Mitigation: Review generated summaries, recommendations, and publishable copy before external use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allinherog-star/skills/xhs-viral-copywriter)
- [Form schema](artifact/references/form-schema.json)
- [Skill metadata](artifact/references/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON runner responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runner responses use a ResultEnvelope contract expected to include summary, items, and artifacts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
