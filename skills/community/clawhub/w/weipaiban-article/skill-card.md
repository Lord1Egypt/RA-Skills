## Description:

将主题或稿件排版为可预览、可继续修改的微信公众号文章，并发布到微排版。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weipaiban](https://clawhub.ai/user/weipaiban)

### License/Terms of Use:

AGPL-3.0

## Use Case:

面向需要制作微信公众号文章的创作者：根据主题或稿件生成带有配色、章节配图及可选交互版式的文章，并发布为可预览和继续编辑的微排版作品。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided images may be sent to an external service, and the security scan reports incomplete coverage.

Mitigation: Only provide images approved for external processing; avoid sensitive images and review the requested API key, file, and network access before use.

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/weipaiban/skills/weipaiban-article)
- [微排版](https://weipaiban.cn)
- [微排版 API 密钥管理](https://weipaiban.cn/settings/api-keys)
- [文章结构与排版](artifact/references/article-structure.md)
- [图片素材流程](artifact/references/assets.md)
- [作品发布格式](artifact/references/api-formats.md)

## Skill Output:

**Output Type(s):** [Code, Files]

**Output Format:** [HTML article content and a published work link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing requires a WEIPAIBAN_API_KEY; images may be selected from the service's asset library or supplied by the user.]

## Skill Version(s):

1.0.3 (source: server release metadata, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
