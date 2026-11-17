## Description:

Sentiment Compass monitors keyword mentions across Chinese social media platforms, analyzes sentiment, generates public-opinion reports, and sends alerts when negative coverage crosses configured thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiji0802](https://clawhub.ai/user/qiji0802)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, brand, and operations teams use this skill to monitor public mentions on major Chinese social platforms, classify sentiment, generate reports, and trigger alerts for negative coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials may be stored in plain text configuration.

Mitigation: Use limited-scope API keys, avoid storing high-value SMTP credentials, and restrict local configuration file permissions before use.

Risk: Monitored social-media content and alert details may be sent to configured third-party services.

Mitigation: Install only when those data flows are acceptable, and verify webhook URLs and notification destinations carefully.

Risk: Runtime dependencies and browser automation packages can change behavior across releases.

Mitigation: Pin dependencies and review updates before production deployment.

## Reference(s):

- [Sentiment Compass on ClawHub](https://clawhub.ai/qiji0802/skills/sentiment-compass)
- [YK-Global](https://yk-global.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, text summaries, command-line output, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sentiment labels, sentiment scores, reason summaries, keyword monitoring settings, and alert details.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
