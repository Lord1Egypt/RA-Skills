## Description:

Control WHEN/WHEN Voice LAN clock devices for voice time announcement, WHEN Voice weather broadcast, alarm CRUD, and countdown timers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[master-gong](https://clawhub.ai/user/master-gong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with WHEN or WHEN Voice LAN clock devices use this skill to query and manage alarms, create timer reminders, and trigger supported voice or weather broadcasts from an agent-driven CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify persistent alarms on configured LAN clock devices.

Mitigation: Use it only with trusted WHEN/WHEN Voice clocks on a trusted LAN, verify configured device IPs, and review existing alarms before set, edit, delete, or timer operations.

Risk: Creating a timer on a device that already has the maximum number of alarms can replace an existing alarm.

Mitigation: Query alarms first with get_alarm and confirm capacity before creating timer reminders.

Risk: An untrusted prompt could try to select an arbitrary configuration file.

Mitigation: Keep configuration files under user control and do not allow prompts to choose arbitrary --config paths.

## Reference(s):

- [WHEN product page](https://iottimer.com/products/when/)
- [WHEN Voice product page](https://iottimer.com/products/when_voice/)
- [WHEN Web API protocol](artifact/docs/WHEN_WEB_API_PROTOCOL.md)
- [WHEN Voice Web API protocol](artifact/docs/WHEN_VOICE_WEB_API_PROTOCOL.md)
- [ClawHub skill page](https://clawhub.ai/master-gong/skills/when-clock-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill executes local Python commands that return JSON on stdout and errors on stderr.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json; artifact SKILL.md frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
