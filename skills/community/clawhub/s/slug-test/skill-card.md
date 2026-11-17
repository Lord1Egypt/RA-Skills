## Description:

Stream and sync iPhone and Apple Watch HealthKit data through a local webhook server for AI analysis, recovery scoring, health trend analysis, and anomaly alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crxiaobailiu-gif](https://clawhub.ai/user/crxiaobailiu-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect iPhone and Apple Watch health data to an agent via a self-hosted webhook, enabling health trend questions, recovery scoring, and anomaly alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publicly exposed webhook and admin routes may expose sensitive health-sync services if they are weakly protected.

Mitigation: Set a strong ADMIN_TOKEN before public exposure and restrict or protect /admin/* routes.

Risk: The setup uses an unpinned executable server dependency.

Mitigation: Use a pinned, auditable server version before installation or deployment.

Risk: Local JSONL and SQLite files contain sensitive health records.

Mitigation: Treat stored health data as sensitive records with encryption, retention limits, secure backups, and least-privileged service execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crxiaobailiu-gif/skills/slug-test)
- [HealthClaw TestFlight beta](https://testflight.apple.com/join/SXDjT6vC)
- [Webhook server API spec](../webhook-server/docs/API_SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, pairing, sync, multi-user, and API endpoint guidance.]

## Skill Version(s):

0.0.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
