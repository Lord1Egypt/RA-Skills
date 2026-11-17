## Description:

Broadcast a message to multiple OpenClaw group sessions simultaneously for cross-agent coordination, alerts, and announcements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to send one coordination, alert, or announcement message to multiple OpenClaw Telegram or Discord group sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadcast messages to multiple Telegram or Discord group targets by default.

Mitigation: Install only where group broadcasting is intended, replace config/groups.json with approved targets, and avoid default all-groups sends.

Risk: Gateway access may allow broad message delivery if the token has more privileges than needed.

Mitigation: Use a least-privilege OPENCLAW_TOKEN for the local OpenClaw gateway.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-agent-broadcast)
- [Publisher profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and delivery receipt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a configured OpenClaw gateway token when sending messages.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
