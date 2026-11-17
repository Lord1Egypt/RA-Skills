## Description:

Coordinates a Xiaodu leave-home routine using the existing xiaodu-control-official skill to shut down selected smart-home devices, summarize weather, calendar, and reminder information, and report what still needs attention before the user leaves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dueros-mcp](https://clawhub.ai/user/dueros-mcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home automation agents use this skill when a user is leaving home and wants a combined device shutdown, weather check, schedule/reminder summary, and lock-handling prompt. It is intended for Xiaodu environments that already have xiaodu-control-official configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Short everyday phrases can trigger smart-home changes.

Mitigation: Use explicit trigger phrases where possible and review the configured device scope before deployment.

Risk: The skill can query and speak schedule or reminder information during the leave-home routine.

Mitigation: Install only in environments where spoken schedule and reminder summaries are acceptable to the user.

Risk: Remembered leave-home preferences can affect future device and lock behavior.

Mitigation: Keep preference files inspectable and deletable, and review or disable automatic lock preferences.

Risk: Door-lock actions are sensitive smart-home operations.

Mitigation: Require an explicit second confirmation before locking unless the user has deliberately configured a reviewed preference.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dueros-mcp/skills/xiaodu-leave-home-mode-official)
- [usage-notes.md](references/usage-notes.md)
- [test-cases.md](references/test-cases.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and natural-language status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update inspectable preference files such as XIAODU_CONTEXT.md or MEMORY.md when the user asks to remember leave-home preferences.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
