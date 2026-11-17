## Description:

Session Guardian helps OpenClaw users protect long-running agent conversations with local scheduled backups, recovery commands, health checks, and collaboration tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1052326311](https://clawhub.ai/user/1052326311)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure local session backups, monitor session health, restore agent conversations after crashes, and track multi-agent collaboration state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled backup and health tasks repeatedly read and store OpenClaw agent conversations, which may contain sensitive content.

Mitigation: Review cron entries before enabling the skill, restrict backup directory permissions, and avoid the daily OpenClaw summary unless model-provider and delivery-channel exposure is acceptable.

Risk: Health-check cleanup and restore features can delete or overwrite session files.

Mitigation: Keep an independent backup of important sessions and test cleanup or restore behavior on noncritical sessions before using it on active work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1052326311/skills/session-guardian)
- [SKILL.md](SKILL.md)
- [README_EN.md](README_EN.md)
- [EXAMPLES.md](EXAMPLES.md)
- [TEST-REPORT-v2.0.md](TEST-REPORT-v2.0.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installed scripts create local backup, health report, collaboration, and restore artifacts under the user's OpenClaw workspace.]

## Skill Version(s):

3.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
