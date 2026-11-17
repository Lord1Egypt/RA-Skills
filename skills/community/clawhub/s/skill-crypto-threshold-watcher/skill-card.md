## Description:

Crypto Threshold Watcher monitors crypto watchlist tokens against configurable price, volume, and RSI thresholds and helps agents emit alerts when entry conditions are met.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading workflow operators use this skill to monitor crypto watchlists and generate actionable threshold alerts for price breakouts, price breakdowns, volume spikes, and RSI conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unbundled threshold-watcher.js script, so runtime behavior cannot be verified from the submitted artifact alone.

Mitigation: Review or supply the actual script before use and verify the script path is absolute and trusted.

Risk: Hourly recurring execution can repeatedly run an unverified trading alert workflow.

Mitigation: Do not enable the recurring task until the implementation is reviewed and operators know how to disable the schedule.

Risk: Telegram alerts may disclose trading watchlists, thresholds, notes, and signals to an external messaging service.

Mitigation: Treat Telegram delivery as external sharing and avoid connecting messaging credentials unless the implementation and recipient scope are trusted.

## Reference(s):

- [Crypto Threshold Watcher on ClawHub](https://clawhub.ai/zero2ai-hub/skills/skill-crypto-threshold-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts may include token symbols, prices, volumes, threshold status, timestamps, and watchlist notes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
