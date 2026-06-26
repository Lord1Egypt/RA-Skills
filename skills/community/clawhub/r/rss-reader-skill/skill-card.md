## Description: <br>
Rss Reader helps an agent manage RSS subscriptions, refresh feeds, generate AI-assisted daily news summaries, and optionally post reports to Feishu or Lark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangluo1](https://clawhub.ai/user/wangluo1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to subscribe to RSS feeds, collect new articles, generate concise AI news digests, and send those digests to a Feishu or Lark channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RSS titles, links, snippets, and generated reports may be processed by the configured AI endpoint and optionally posted to Feishu or Lark. <br>
Mitigation: Use only feeds and reports that are acceptable to share with those configured services. <br>
Risk: Default or user-added feeds may include private or internal sources. <br>
Mitigation: Review the feed list before use and avoid private/internal feeds unless that sharing is approved. <br>
Risk: Controlled deployments depend on third-party Python packages and outbound service endpoints. <br>
Mitigation: Pin and audit dependencies and verify the configured AI and webhook endpoints before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangluo1/rss-reader-skill) <br>
- [Artifact README](artifact/README.md) <br>
- [Zhipu AI platform](https://open.bigmodel.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown reports with article links plus text status messages and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured RSS feeds, an AI API endpoint, and an optional Feishu or Lark webhook; stores subscriptions and article records as local JSON files.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
