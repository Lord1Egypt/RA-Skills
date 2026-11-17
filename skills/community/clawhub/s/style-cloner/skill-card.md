## Description:

提供1-5篇参考文章和原始素材，分析参考文章的写作风格并将素材改写为同风格的3个版本，支持强度调节和迭代优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to analyze reference articles, rewrite draft material in a similar writing style, and compare three style-strength variants for publication or further editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and writing samples may be sent to an unintended external LLM provider if the API base is misconfigured.

Mitigation: Use a provider-specific API key, explicitly set the matching API base, and avoid custom API_BASE values unless the endpoint is trusted.

Risk: Reference articles and draft content may contain confidential or sensitive material that is sent to the configured LLM provider.

Mitigation: Do not provide confidential drafts or reference articles unless sharing them with the configured provider is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antonia-sz/skills/style-cloner)
- [Publisher Profile](https://clawhub.ai/user/antonia-sz)
- [Default DeepSeek API Endpoint](https://api.deepseek.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with a style analysis summary, three rewritten article versions, and usage suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save the generated Markdown result to a user-specified output file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
