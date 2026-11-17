## Description:

ClawDoctor monitors OpenClaw gateway, cron, session, auth, and cost health, sends Telegram alerts, and can restart the gateway when it goes down.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relayplane](https://clawhub.ai/user/relayplane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running OpenClaw use this skill to install and operate ClawDoctor for proactive health monitoring, Telegram alerts, and optional gateway recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm installation and daemon execution can run package code with local user privileges.

Mitigation: Use only a reviewed exact package version from a trusted publisher before installing or starting the daemon.

Risk: The daemon reads OpenClaw operational files and may create or change user service and configuration files.

Mitigation: Run it only on intended OpenClaw hosts, inspect generated config and service files, and begin with dry-run mode.

Risk: Supplying Telegram tokens on the command line can expose secrets through shell history or process listings.

Mitigation: Avoid command-line tokens; prefer an reviewed configuration or secret-handling flow.

Risk: Automatic gateway restart can disrupt service if enabled before behavior is validated.

Mitigation: Validate monitor output in dry-run mode before enabling auto-fix behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/relayplane/skills/relayplane-clawdoctor)
- [ClawDoctor site](https://clawdoctor.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes npm installation commands, daemon commands, setup options, monitoring behavior, and operational risk guidance.]

## Skill Version(s):

0.4.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
