## Description:

Monitor and analyze Home Assistant energy consumption by room, identify high power consumers, and draft Home Assistant automations based on configured power thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liverock](https://clawhub.ai/user/liverock)

### License/Terms of Use:

MIT-0

## Use Case:

External Home Assistant users and automation developers use this skill to inspect live energy consumption, compare device or area usage, and draft reviewable power-threshold automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a long-lived Home Assistant token.

Mitigation: Use a dedicated least-privilege token when possible, keep it in the environment, and rotate it if it may have been exposed.

Risk: The default Home Assistant URL uses plaintext HTTP.

Mitigation: Configure HTTPS for Home Assistant before using the skill with sensitive or remote deployments.

Risk: The skill reads all visible Home Assistant states during discovery, not only energy sensors.

Mitigation: Run it only against Home Assistant accounts and instances where broad visible-state access is acceptable.

Risk: Generated automation drafts can target switch actions for real devices.

Mitigation: Review every action, target entity, threshold, time condition, and occupancy condition before applying any generated automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liverock/skills/smart-home-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Text summaries, Markdown tables, and Home Assistant automation JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selectable output formats are summary, table, and automation; the default formats are summary and table.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
