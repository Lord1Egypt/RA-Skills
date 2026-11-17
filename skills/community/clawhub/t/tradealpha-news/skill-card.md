## Description:

获取 TradeAlpha 实时新闻和语义检索结果，适用于按来源、主题、事件、公司或叙事检索相关新闻，并在当前会话中使用用户提供的 TradeAlphaToken 查询结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tradealpha-coder](https://clawhub.ai/user/tradealpha-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to query TradeAlpha realtime news and semantic news search results, then receive concise Chinese summaries and structured request/result details. It is intended for news lookup workflows after the user supplies a TradeAlpha API token in the current chat session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to paste a TradeAlpha API token into chat and reuses it during the current session.

Mitigation: Use a scoped or short-lived token when possible, avoid account-wide credentials, and never write the token to files, environment variables, shell commands, or local configuration.

Risk: The skill may trigger on broad news requests involving sources such as Reuters, Bloomberg, Truth, domestic news, or research reports.

Mitigation: Confirm the user wants a TradeAlpha lookup before requesting a token or making an API call.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tradealpha-coder/skills/tradealpha-news)
- [TradeAlpha News Reference](references/reference.md)
- [Conversation and Payload Examples](references/examples.md)
- [TradeAlpha Account and Token Site](https://quantaccess.lxaa.top/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, JSON, guidance]

**Output Format:** [Chinese Markdown summaries with structured JSON request and result details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided TradeAlphaToken in chat; the token is reused only within the current session and should not be written to files, environment variables, shell commands, or local configuration.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 2.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
