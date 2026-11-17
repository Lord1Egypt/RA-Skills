## Description:

微信公众号文章搜索与解析。搜狗微信+新榜双源搜索，Python脚本解析全文（零Node依赖），Serper转载兜底。

This skill is ready for commercial/non-commercial use.

## Publisher:

[langhuachuanshi](https://clawhub.ai/user/langhuachuanshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations agents use this skill to search WeChat public-account articles, parse article text and images, score and de-duplicate results, and publish selected content to a knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and article metadata may be sent to Sogou, Serper, and article-source sites.

Mitigation: Use the skill only where those external requests are acceptable, and review search terms before execution.

Risk: Collected content can be written persistently to Feishu knowledge-base destinations.

Mitigation: Require explicit confirmation before Feishu writes and verify the target directory before publishing.

Risk: The workflow can fetch user- or agent-selected article URLs without a stated allowlist.

Mitigation: Add URL allowlisting for approved search and article domains before unattended use.

Risk: Runtime Python dependencies are not pinned in the artifact.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/langhuachuanshi/skills/silas-wechat-article-search)
- [Example search output](references/example-output.json)
- [Sogou WeChat search endpoint](https://weixin.sogou.com/weixin?type=2&query=%E5%85%B3%E9%94%AE%E8%AF%8D)
- [Serper search endpoint](https://google.serper.dev/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash examples, Python parser usage, and JSON article records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPER_API_KEY for Serper fallback; parser output can be printed or saved as JSON.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
