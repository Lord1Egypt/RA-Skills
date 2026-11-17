## Description:

Scrapfly Alerting helps agents configure and manage threshold-based alerts on Scrapfly account metrics through REST API, MCP tools, or the Scrapfly CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapfly](https://clawhub.ai/user/scrapfly)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operations teams use this skill to set up, preview, test, snooze, update, and delete Scrapfly metric alerts. It guides agents to ground thresholds in observed account behavior before creating alert rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scrapfly API keys may be exposed if users paste real credentials into REST examples or URLs.

Mitigation: Prefer MCP or CLI workflows that keep credentials out of URLs, and redact API keys from prompts, logs, and examples.

Risk: Webhook signing keys returned by alert reads can be exposed through agent output or logs.

Mitigation: Treat webhook signing keys as secrets, redact them when displaying alert details, and rotate them if exposure is suspected.

Risk: Create, update, delete, snooze, unsnooze, and test actions can change alert behavior or trigger notifications.

Mitigation: Use preview and dry-run steps first, then require explicit user confirmation before committing alert mutations.

## Reference(s):

- [Scrapfly Alerting Concept Guide](https://scrapfly.io/docs/alerting/getting-started)
- [Scrapfly Alerting Metric Registry](https://scrapfly.io/docs/alerting/metric-reference)
- [Scrapfly Alerting State Machine](https://scrapfly.io/docs/alerting/state-machine)
- [Scrapfly Alerting Webhook Payload and Signing](https://scrapfly.io/docs/alerting/webhook-payload)
- [Scrapfly Alerting Error Reference](https://scrapfly.io/docs/alerting/error-reference)
- [Scrapfly Alerting Anti-Spam Controls](https://scrapfly.io/docs/alerting/anti-spam)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, HTTP, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run, confirmation, and preview guidance for alert changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
