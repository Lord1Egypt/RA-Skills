## Description:

Monitors public Telegram channels via web scraping, extracts new messages, generates AI-powered summaries, and delivers structured digests to a configured OpenClaw notification channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rodionkertling](https://clawhub.ai/user/rodionkertling)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor public Telegram channels, detect new posts, summarize updates with an LLM, and receive a digest through their configured OpenClaw notification channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitored Telegram message text can be sent to a configured LLM endpoint for summarization.

Mitigation: Use only trusted HTTPS or loopback LLM gateways and avoid monitoring sensitive channels unless external processing is acceptable.

Risk: A gateway token may be exposed to configurable LLM endpoints.

Mitigation: Restrict and rotate OPENCLAW_GATEWAY_TOKEN and review the configured gateway before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rodionkertling/skills/tg-news-digest-lite)
- [Telegram public channel web view](https://t.me/s/{channel})
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown or plain text digest plus JSON status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Digest length, language, grouping, monitored channels, fetch window, and notification channel are configurable.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, skill.yaml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
