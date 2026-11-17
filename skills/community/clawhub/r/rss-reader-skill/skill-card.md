## Description:

RSS Reader manages RSS subscriptions, refreshes feeds, generates AI news summaries and daily trend reports, and can push reports to Feishu or Lark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangluo1](https://clawhub.ai/user/wangluo1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain RSS subscriptions, collect new article links, and produce concise AI-generated news summaries or daily briefings. It is useful for personal or team news monitoring workflows that may optionally publish reports to Feishu or Lark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly fetch arbitrary RSS URLs, including user-added feeds.

Mitigation: Use only public feed URLs and avoid localhost, private-network, or internal service addresses.

Risk: RSS titles, links, summaries, and generated reports may be sent to configured AI and Feishu/Lark services.

Mitigation: Use public or non-sensitive feeds, review configured sharing destinations, and install only when this data flow is acceptable.

Risk: The AI API base URL is configurable, which can route API keys and RSS-derived content to an untrusted provider if changed incorrectly.

Mitigation: Keep OPENAI_BASE_URL fixed to a trusted provider and protect OPENAI_API_KEY and FEISHU_WEBHOOK_URL values.

Risk: Automatic refresh can run repeatedly through cron and amplify external requests or data sharing.

Mitigation: Review the cron command and refresh interval before enabling scheduled execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangluo1/skills/rss-reader-skill)
- [feedparser](https://github.com/kurtmckee/feedparser)
- [Zhipu AI API](https://open.bigmodel.cn/)
- [OpenAI-compatible API endpoint](https://api.openai.com/v1)
- [Feishu Bot Webhook Endpoint](https://open.feishu.cn/open-apis/bot/v2/hook/xxx)
- [Lark Bot Webhook Endpoint](https://open.larksuite.com/open-apis/bot/v2/hook/xxx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with RSS links, summaries, trend analysis, and configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports include article titles, source names, recommended readings, concise trend summaries, and original links.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
