## Description:

图文运营创作器帮助内容运营、品牌和编辑完成链接仿写、Skill 推广文生成、正文补图与文章质检。

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, brand teams, skill developers, bloggers, and editors use this skill to create operations articles, rewrite articles from a source link, generate Skill promotional long-form content, add illustrations to existing drafts, and receive an article quality report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to user-provided sites and redfox.hk.

Mitigation: Use only public source URLs, avoid internal or private URLs, and run the skill in a sandboxed workspace.

Risk: The skill may use a local RedFox API key fallback file.

Mitigation: Prefer explicit REDFOX_API_KEY configuration and remove or disable ~/.qoder/apis/redfox.json when every API key use must be intentional.

Risk: Drafts, links, and generated assets may include unpublished or confidential content.

Mitigation: Do not provide confidential unpublished material unless the workspace and RedFox service use are approved for that content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/if530770/skills/visual-ops-writer)
- [Core Workflow](artifact/references/core_workflow.md)
- [Writing Framework](artifact/references/writing-framework.md)
- [Article Type Templates](artifact/references/article-type-templates.md)
- [Image Decision Rules](artifact/references/image-decision-rules.md)
- [Link Rewrite Guide](artifact/references/link-rewrite-guide.md)
- [Prompt Templates](artifact/references/prompt-templates.md)
- [Error Handling](artifact/references/error-handling.md)
- [Persona Matrix](artifact/references/persona-matrix.md)
- [RedFoxHub API Keys](https://redfox.hk/settings/api-keys?source=github)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown article with embedded image links, JSON quality report, generated image files or URLs, and conversational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated articles are typically saved as article.md; quality checks are reported in validation_report.json; image generation requires REDFOX_API_KEY and can be skipped or degraded when the key is unavailable.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
