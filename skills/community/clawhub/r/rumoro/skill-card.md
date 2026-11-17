## Description:

Helps an OpenClaw agent track and summarize public mentions of brands, competitors, and topics through Rumoro, and manage related alerts and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markolo10](https://clawhub.ai/user/markolo10)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and individuals use this skill with an OpenClaw agent to monitor brand and competitor mentions, prioritize responses, review trends and people, and configure notifications through Rumoro.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A write-scoped API key can change tracked keywords, alerts, channels, people records, and other workspace data.

Mitigation: Use a read-only key for analysis; grant write access only when changes are needed and confirm consequential changes with the user.

Risk: Alerts can send collected mention content to external Slack, email, Telegram, or webhook destinations.

Mitigation: Review destination settings and intended recipients before enabling alerts or testing deliveries.

## Reference(s):

- [Rumoro OpenClaw integration guide](https://docs.rumoro.dev/integrations/openclaw)
- [Rumoro API reference](https://api.rumoro.dev/v1/openapi.json)
- [Rumoro documentation](https://docs.rumoro.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Plain-language summaries and instructions, optionally with commands or structured API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include links to public posts, mention summaries, analytics, and alert setup guidance.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
