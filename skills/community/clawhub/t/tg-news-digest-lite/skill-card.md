## Description: <br>
Monitors public Telegram channels via web scraping (t.me/s/*), extracts new messages, generates AI-powered summaries, and delivers structured digests to a configured OpenClaw notification channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rodionkertling](https://clawhub.ai/user/rodionkertling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers who track public Telegram channels use this skill to monitor configured channels, summarize new posts with a chosen LLM gateway, and send a digest to an OpenClaw notification channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public Telegram post text from monitored channels is sent to the configured OpenClaw or LLM gateway. <br>
Mitigation: Use only trusted gateway providers and monitor only channels whose public text is acceptable to process through that provider. <br>
Risk: The gateway URL and token affect where summaries are generated and may expose sensitive access to the configured LLM service. <br>
Mitigation: Review OPENCLAW_GATEWAY_URL and OPENCLAW_GATEWAY_TOKEN before installation and rotate the token if provider access changes. <br>
Risk: Channel removal changes local configuration and cache state persistently. <br>
Mitigation: Review channel changes deliberately and back up config.yaml or state data before large monitoring-list changes. <br>


## Reference(s): <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Configuration example](artifact/config.example.yaml) <br>
- [ClawHub release page](https://clawhub.ai/rodionkertling/tg-news-digest-lite) <br>
- [Telegram public channel web pages](https://t.me/s/{channel}) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, JSON, Configuration] <br>
**Output Format:** [Markdown or plain text digests plus JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digest language, monitored channels, token cap, grouping, and notification channel are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
