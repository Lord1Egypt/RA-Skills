## Description:

Six-dimension evolution system for AI agents. Transform from reactive assistant to proactive partner with lessons tracking, success patterns, decision review, preference tracking, skill statistics, and knowledge gap detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephongao](https://clawhub.ai/user/stephongao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install a six-file memory and review system that tracks lessons, successes, decisions, preferences, skill statistics, and knowledge gaps for ongoing agent improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent memory and scheduled review workflows from conversation-derived data.

Mitigation: Enable it only after explicit user approval, define which session files may be read, and provide a documented way to review, disable, or delete stored memories.

Risk: The daily review workflow can push full reports to Feishu without clear redaction or destination controls.

Mitigation: Remove or gate the Feishu push step unless the destination, consent model, and redaction requirements are configured and reviewed.

Risk: Automated updates to memory and preference files may introduce incorrect or conflicting user profile information.

Mitigation: Require consistency checks and human review for conflicting memory, preference, or decision updates before they are written.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stephongao/skills/six-dimension-evolution)
- [Publisher profile](https://clawhub.ai/user/stephongao)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace memory, review, preference, decision, skill statistics, knowledge gap, and heartbeat task files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
