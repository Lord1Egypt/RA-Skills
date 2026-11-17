## Description:

Uses Shenlan News public APIs to analyze financial content for sentiment, summaries, keywords, interpretation, fact checks, market impact, AI editorial feeds, and article text-to-speech.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenlannews](https://clawhub.ai/user/shenlannews)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve AI-generated financial-news analysis, browse Shenlan AI editor content, and request audio versions of articles through Shenlan News public HTTPS APIs. Outputs should be treated as informational financial content, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes HTTPS requests to Shenlan News public APIs for financial-news analysis, AI editor feeds, and text-to-speech.

Mitigation: Install only when this expected network behavior is acceptable for the deployment environment.

Risk: Financial analysis outputs may be mistaken for investment advice.

Mitigation: Present results as informational content and preserve the skill's guidance that AI analysis does not constitute investment advice.

Risk: Text-to-speech requests may generate or return remote audio links.

Mitigation: Ask explicitly before generating TTS audio and disclose returned audio links to the user.

## Reference(s):

- [深蓝 AI 分析师 API 参考文档](references/api-reference.md)
- [Shenlan News Homepage](https://www.shenlannews.com)
- [ClawHub Skill Page](https://clawhub.ai/shenlannews/skills/shenlan-ai-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and JSON-backed API response summaries, with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote article audio links returned by the Shenlan News TTS API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
