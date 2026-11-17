## Description:

A guidance-only setup skill that helps an agent, after explicit user consent and backup, modify a local openclaw-weixin plugin so quoted bot messages can be injected as context for follow-up questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yechang1450](https://clawhub.ai/user/yechang1450)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill when they want the local WeChat channel to understand follow-up questions that quote a bot reply. The agent follows a consent, backup, implementation, restart, verification, and rollback workflow for that local plugin change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to modify a local WeChat channel plugin.

Mitigation: Require explicit user confirmation, readable backups, deterministic build steps, restart verification, and documented rollback before and after any change.

Risk: Quote matching may store recent bot message text locally.

Mitigation: Keep the index local with owner-only permissions, enforce expiry and per-recipient caps, avoid logging message bodies, and provide clear disable and cleanup steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yechang1450/skills/weixin-quote)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code-editing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces implementation and verification guidance; it does not ship a patch file or plugin package.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
