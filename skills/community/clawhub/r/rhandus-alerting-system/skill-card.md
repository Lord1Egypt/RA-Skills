## Description:

Centralized alerting and notification system for OpenClaw. Multi-channel alerts, intelligent rules, escalation, and audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhanxerox](https://clawhub.ai/user/rhanxerox)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to define alerts, monitor endpoints and system signals, send notifications, track active incidents, and resolve alert history in OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-based command construction and monitor paths may execute unsafe commands or handle untrusted endpoint values.

Mitigation: Review and replace shell command construction with structured process APIs, strict argument handling, endpoint allowlists, and payload redaction before installation.

Risk: System-level persistence and writes into other skills can modify the host environment beyond ordinary alerting behavior.

Mitigation: Use explicit user-scoped scheduling, document privileged actions and uninstall steps, and disable automatic cross-skill file writes unless reviewed and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rhanxerox/skills/rhandus-alerting-system)
- [Publisher profile](https://clawhub.ai/user/rhanxerox)
- [Tiklick website](https://tiklick.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented text with shell commands and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate alert records, logs, notification payloads, integration snippets, and monitoring status summaries.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
