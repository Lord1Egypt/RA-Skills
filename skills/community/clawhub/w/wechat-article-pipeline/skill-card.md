## Description:

编排微信公众号文章的写作策略、HTML 主稿、独立 AI 写作风险审核、配图确认、样式审核和微信排版预览。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacktian89](https://clawhub.ai/user/zacktian89)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, and marketing teams use this skill to run a guided or automatic WeChat article production flow from topic planning through HTML draft generation, AI-writing-risk review, image selection, style review, and final preview or copy-ready HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic mode can continue through drafting, AI-risk review, image research, revisions, and preview generation without repeated confirmations.

Mitigation: Review the initial auto-run choice and inspect the final draft, review summary, image notes, and preview before copying content into WeChat or publishing.

Risk: Generated article drafts can contain incorrect, outdated, or insufficiently sourced factual claims.

Mitigation: Verify important facts, quotes, policies, and time-sensitive claims against authoritative sources before using the final HTML.

Risk: Images found or provided during the workflow can carry copyright, attribution, likeness, or context risks.

Mitigation: Use only images with confirmed source, authorization, and attribution status, and remove unconfirmed placeholders before final delivery.

Risk: Draft language can retain visible AI-writing patterns or platform-inappropriate style despite revision.

Mitigation: Use the required independent AI-writing-risk review and stop for human review if repeated review rounds still report medium or high risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zacktian89/skills/wechat-article-pipeline)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact OpenAI agent metadata](artifact/agents/openai.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Markdown response with HTML code or a generated local HTML preview file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an AI-writing-risk summary, image source and authorization notes, style review status, and unresolved factual or copyright risks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
