## Description:

Lets an external Agent Skills tool query an OpenClaw gateway or, with explicit user direction and confirmation for side effects, dispatch work to named agents and send messages through named channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT

## Use Case:

Developers using Claude Code, Codex, OpenCode, Trae, DSH, or another Agent Skills tool can use this skill to query an OpenClaw gateway, identify its agents, dispatch a user-requested task, or send a user-approved channel message. It is intended to activate only when the user names the OpenClaw action and its target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial: three local references were unresolved and the PNG was outside the static analyzers' scope.

Mitigation: Review the unresolved references and image asset before installation, alongside the scanner's stated coverage limits.

Risk: Dispatching an agent can cause downstream file or messaging effects, and sending through a channel is externally visible.

Mitigation: Require user confirmation of the exact agent and task, or channel, recipient, and message, before dispatching or sending.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-commander)
- [XiaoyaoClaw product page](https://www.xiaoyaosai.com/xiaoyaoclaw/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Status information, Text]

**Output Format:** [Markdown guidance with shell command examples and returned status or task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language; command and output formats follow the CLI requirements.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
