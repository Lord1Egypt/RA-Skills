## Description:

微信公众号文章处理工具 - 自动抓取、结构化整理、保存到飞书文档。触发词：处理公众号文章、微信文章转飞书、公众号链接

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoyaryyj](https://clawhub.ai/user/hoyaryyj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to turn WeChat public account article links into structured article notes and Feishu documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat article content may be sent to and stored in Feishu.

Mitigation: Use only content the user is authorized to process, avoid sensitive or access-controlled articles, and confirm Feishu document permissions before saving.

Risk: Some WeChat articles may require login or present verification challenges, which can prevent complete extraction.

Mitigation: Ask the user to provide the article text manually or complete access steps when the article cannot be fetched.

Risk: Automated extraction and summarization can omit or misstructure parts of an article.

Mitigation: Review the structured notes and Feishu document before sharing or relying on the processed content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hoyaryyj/skills/wechat-article-processor)
- [ClawHub publisher profile](https://clawhub.ai/user/hoyaryyj)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown article notes and a Feishu document link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided WeChat article URL and Feishu authorization.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
