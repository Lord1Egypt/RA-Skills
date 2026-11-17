## Description:

Advanced RUNSTR fitness analytics with trend analysis, performance insights, training recommendations, and correlation tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katla50](https://clawhub.ai/user/katla50)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and RUNSTR users use this skill to analyze workout history, habits, mood, and steps from encrypted Nostr backup data, producing coaching insights, trend analysis, personal records, and training recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a full Nostr private key and decrypted RUNSTR health or journal data.

Mitigation: Install only on a trusted personal system, avoid pasting the key into chat or passing it with --nsec on shared or monitored systems, and remove cached data under ~/.cache/runstr-analytics when it is no longer needed.

Risk: The optional cron workflow can repeatedly fetch and process private fitness data in the background.

Mitigation: Review the cron entry before enabling it, confirm logs and cache paths are acceptable, and use disk encryption or equivalent local data protection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katla50/skills/runstr-analytics)
- [nak CLI package](https://github.com/fiatjaf/nak)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal reports, JSON exports, Markdown reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read encrypted Nostr backups, write local SQLite cache data, and create optional cron-based daily reports.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
