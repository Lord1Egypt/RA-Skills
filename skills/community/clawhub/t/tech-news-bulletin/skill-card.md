## Description:

Collect latest technology and AI news from RSS feeds and the TLDR.tech AI newsletter, merge them into a unified daily digest, and send via email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juniarto-samsudin](https://clawhub.ai/user/juniarto-samsudin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect technology and AI news from RSS feeds and TLDR.tech AI, deduplicate and summarize articles, and send a daily HTML email bulletin to configured recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a user's SMTP account to email hard-coded third-party recipients.

Mitigation: Review and replace EMAIL_ADDRESSES before running, confirm intended recipients, and use least-privilege SMTP or app credentials.

Risk: The skill fetches feed-controlled article URLs and sends article text to a configured Ollama endpoint.

Mitigation: Restrict RSS sources, article fetching, and the Ollama endpoint to trusted destinations before installation or scheduled execution.

Risk: Scheduled execution can repeatedly send the bulletin once enabled.

Mitigation: Keep any cron job disabled until SMTP credentials, recipients, and content sources have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juniarto-samsudin/skills/tech-news-bulletin)
- [TLDR AI newsletter](https://tldr.tech/ai/)
- [TechCrunch RSS feed](https://techcrunch.com/feed/)
- [WIRED AI RSS feed](https://www.wired.com/feed/tag/ai/latest/rss)

## Skill Output:

**Output Type(s):** [text, HTML, shell commands, configuration, guidance]

**Output Format:** [HTML email digest with supporting Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured SMTP credentials and Python dependencies; may fall back to feed snippets if the local Ollama summarizer is unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
