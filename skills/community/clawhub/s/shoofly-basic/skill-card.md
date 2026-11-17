## Description:

Shoofly Basic monitors AI agent tool calls for prompt injection, tool response injection, out-of-scope writes, runaway loops, and data exfiltration signals, then logs and sends alerts without blocking execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wow-leeroy-jenkins05](https://clawhub.ai/user/wow-leeroy-jenkins05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to monitor agent tool activity for suspicious behavior and receive notifications while allowing the session to continue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes agent behavior globally by asking the agent to monitor every tool call and persist broad tool-call data.

Mitigation: Review the skill before installing, enable it only for projects where continuous local logging is acceptable, and periodically inspect or rotate ~/.shoofly/logs/alerts.log.

Risk: Alerts may include sensitive project context and can be sent through configured external messaging channels.

Mitigation: Avoid external channels for sensitive projects unless alert content is redacted and channel targets are explicitly approved.

Risk: The security evidence recommends fixing the notifier script before use.

Mitigation: Review and correct the notifier behavior in bin/shoofly-notify.sh, then test each configured notification channel before enabling the skill.

Risk: The bundled warning text includes promotional content that may be inappropriate for operational security alerts.

Mitigation: Remove or replace promotional alert text before deployment so notifications contain only actionable security information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wow-leeroy-jenkins05/skills/shoofly-basic)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with JSONL log entries and shell-based notifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and curl; alerts may be written locally and sent through configured terminal, OpenClaw, Telegram, WhatsApp, Discord, desktop, or macOS notification channels.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
