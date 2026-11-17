## Description:

使用红鸦 API 创作小红书图文、制作 Live 实况图片，或检测和修改文案敏感词；支持商品档案及个人词库。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxuux](https://clawhub.ai/user/xiaoxuux)

### License/Terms of Use:

MIT

## Use Case:

External creators and social media marketers use this agent to draft Xiaohongshu posts and page images, turn photos into Live Photos, and review or revise sensitive wording through their RedYA account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to RedYA's external API using the user's API key, and generation can use account credits.

Mitigation: Only provide a key for a service you trust, and review the current charges before requesting paid generation.

Risk: The security review was benign with medium confidence, but reference checks were incomplete and it noted a possible instruction-scope issue.

Mitigation: Review the skill and any unresolved references before use; follow its draft-and-confirm flow before generating paid images.

## Reference(s):

- [ClawHub release](https://clawhub.ai/xiaoxuux/skills/redya-xiaohongshu)
- [RedYA platform](https://hy.ithinkai.cn)
- [Live Photo saving guide](https://hy.ithinkai.cn/tools/live-photo/save)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration instructions]

**Output Format:** [Markdown with generated post copy, image lists, review findings, and setup guidance; may also deliver generated image or Live Photo files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated work may use the user's RedYA account credits.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
