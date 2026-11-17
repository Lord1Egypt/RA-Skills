## Description:

Creates reminder jobs, local backup checks, and daily schedule briefings for OpenClaw users across configured messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayting511](https://clawhub.ai/user/jayting511)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to create reminders from explicit requests or detected schedule details, receive daily schedule briefings, and keep a local backup reminder path if the primary Gateway path is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent OS-level scheduled jobs that can keep running after setup.

Mitigation: Review the installation behavior before use and be prepared to remove cron or LaunchAgent entries during uninstall or deactivation.

Risk: Stored reminder details can be sent through configured messaging channels.

Mitigation: Configure only intended channels and recipients, and avoid storing sensitive schedule content unless that delivery path is acceptable.

Risk: Reminder data and logs are stored locally under the user's OpenClaw data directory.

Mitigation: Protect local data files and review or delete reminder state and logs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayting511/skills/schedule-reminder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured cron and message tools, a local userId, and access to the OpenClaw CLI for primary reminder and messaging actions.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
