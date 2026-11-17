## Description:

智能创作、提取微信公众号文章、生成封面并发布到微信公众号草稿箱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[majiabin2020](https://clawhub.ai/user/majiabin2020)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, operators, and developers use this skill to draft or rewrite Chinese WeChat Official Account articles, generate cover images, preview formatted output, and create drafts or publish when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft or publish commands can send account content before adequate human review.

Mitigation: Use dry-run mode for article generation and preview, review the Markdown and HTML output, and reserve publishing commands for explicit approved requests.

Risk: Configured WeChat and image-provider credentials enable network actions and account usage.

Mitigation: Store credentials with least privilege, apply spending or account controls where available, and run the skill in a controlled environment with restricted outbound network access where practical.

Risk: Material upload commands can transmit local files to WeChat.

Mitigation: Limit accessible working directories and review file paths before running material, draft, or workflow commands that upload files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/majiabin2020/skills/wechat-official-account-article-auto-publisher)
- [CREATION_GUIDE.md](artifact/CREATION_GUIDE.md)
- [SKILL.md](artifact/SKILL.md)
- [title_to_article.md](artifact/templates/prompts/title_to_article.md)
- [rewrite.md](artifact/templates/prompts/rewrite.md)
- [publish_checklist.md](artifact/templates/conversation/publish_checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown articles, JSON command output, HTML previews, cover image files, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local output files and call WeChat or image-generation APIs when credentials are configured; dry-run mode keeps work local for review.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
