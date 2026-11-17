## Description:

Automatically monitors and displays session status information, including token usage, model information, context usage, and feature status, with toggles and display format options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangdaowan](https://clawhub.ai/user/yangdaowan)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to add model, token, and context usage status to agent responses and to manage display preferences through commands, environment variables, or local configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect automatic hook or slash-command integration even though that integration is not visible in the inspected artifact.

Mitigation: Confirm platform hook and command wiring separately before relying on automatic response injection.

Risk: The skill writes display preferences to session_monitor_config.json in the OpenClaw workspace.

Mitigation: Install it only in the intended workspace and review local configuration changes before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yangdaowan/skills/session-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text or Markdown status snippets with optional shell command examples and JSON-backed configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status strings can be compact or detailed and may be inserted at the top, bottom, or inline when session data is provided.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
