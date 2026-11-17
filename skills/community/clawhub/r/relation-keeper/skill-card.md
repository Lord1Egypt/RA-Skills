## Description:

Relation Keeper helps an OpenClaw agent record social contacts, upcoming birthdays or appointments, and past shared experiences so they can be recalled and surfaced as reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujintang](https://clawhub.ai/user/yujintang)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users use this skill to maintain relationship notes, remember birthdays and appointments, archive shared events, and query prior interactions with people in their social network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist sensitive personal data such as addresses, phone numbers, birthdays, and relationship history.

Mitigation: Store data in a private user-controlled RELATION_KEEPER_DATA directory with restrictive permissions, avoid unnecessary sensitive fields, and delete stale JSON records when no longer needed.

Risk: Installation can create a recurring OpenClaw cron task that scans reminders automatically.

Mitigation: Review the install behavior before running npm install, confirm the cron entry after installation, and remove the task if the skill is disabled.

Risk: The security review notes weak scoping and safeguards around relationship data.

Mitigation: Limit use to trusted local environments and review stored data and reminder channels before relying on the skill for ongoing reminders.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yujintang/skills/relation-keeper)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Plain text or Markdown responses with JSON data records and shell command snippets when configuration is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local JSON files for portraits, future events, past events, and sent reminder state.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
