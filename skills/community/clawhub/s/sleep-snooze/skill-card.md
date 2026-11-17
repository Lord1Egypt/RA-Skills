## Description:

Snooze incoming notifications during your sleep window and receive a morning digest when you wake up. Supports Telegram, WhatsApp, and any provider OpenClaw is connected to.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hardik500](https://clawhub.ai/user/hardik500)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to pause routine notifications during configured sleep hours, queue messages locally, let urgent or VIP messages through, and receive a morning digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can suppress notifications across connected providers.

Mitigation: Confirm sleep and wake schedules, VIP bypass rules, and urgent keyword handling before relying on it for important messages.

Risk: The skill stores private message contents locally for the morning digest.

Mitigation: Review local data retention, file permissions, and cleanup behavior for the SQLite queue and related data files before installation.

Risk: The skill registers cron jobs and digest delivery may fail or be delayed if the local environment is misconfigured.

Mitigation: Verify cron registration, Node.js availability in cron, digest delivery confirmation, and uninstall cleanup behavior during setup.

## Reference(s):

- [Setup Guide](references/setup.md)
- [ClawHub Skill Page](https://clawhub.ai/hardik500/skills/sleep-snooze)
- [Metadata Homepage](https://github.com/Hardik500/sleep-snooze)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local schedule, queue, VIP contact, and digest state files under the user's OpenClaw skill data directory.]

## Skill Version(s):

1.0.2 (source: package.json, server release metadata, and target metadata; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
