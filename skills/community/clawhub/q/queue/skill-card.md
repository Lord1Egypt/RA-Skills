## Description:

Queue helps agents manage local, timestamped task and activity logs with commands for adding, planning, tracking, prioritizing, reviewing, searching, and exporting entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external agent users can use Queue to keep a lightweight local work log for task planning, status review, prioritization, reminders, tagging, and throughput summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a durable message queue with retry or delivery guarantees.

Mitigation: Use it only as a lightweight local text-log tracker for planning, reviewing, and exporting task activity.

Risk: Free-form queue entries and exported CSV, JSON, or TXT files may expose sensitive payloads or be mishandled in spreadsheet tools.

Mitigation: Do not store secrets or sensitive operational data in queue entries, and review exports before sharing or opening them in external applications.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [Queue on ClawHub](https://clawhub.ai/bytesagain-lab/skills/queue)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples; runtime output is local text logs and optional JSON, CSV, or TXT exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores data under ~/.local/share/queue and writes exports from the local log data.]

## Skill Version(s):

2.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
