## Description:

Pushman helps agents safely send, inspect, and diagnose personal iPhone notifications through Pushman MCP tools or the installed Pushman CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitekiwi](https://clawhub.ai/user/whitekiwi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send requested notifications to their own iPhone devices, inspect Pushman device/history/usage/status information, and configure local Pushman MCP or CLI workflows while preserving explicit authorization and credential boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A send may create a real user-visible iPhone notification and consume monthly send allowance.

Mitigation: Send only when the current request authorizes one exact notification, report server acceptance without claiming delivery or user-open state, and avoid automatic retries after ambiguous outcomes.

Risk: Login, pairing, rename, and logout change account authorization or credential state.

Mitigation: Run those operations only after explicit user authorization, let the CLI handle credential storage, and verify status after credential changes.

Risk: Notification content, device names, URLs, history, and credentials may contain private user data.

Mitigation: Retrieve and repeat only what the task needs, avoid exposing tokens or keyring credentials, and keep send-only tokens out of command arguments, logs, code, and MCP configuration.

## Reference(s):

- [Pushman safety model](references/safety.md)
- [Pushman CLI installation guide](https://github.com/WhiteKiwi/pushman-cli/blob/main/docs/INSTALL.md)
- [Pushman ClawHub listing](https://clawhub.ai/whitekiwi/skills/pushman)
- [whitekiwi ClawHub publisher profile](https://clawhub.ai/user/whitekiwi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Pushman server acceptance IDs, target counts, status facts, usage facts, diagnostic findings, or MCP configuration guidance; avoids exposing private notification content, device names, URLs, tokens, or credential values unless required for the current request.]

## Skill Version(s):

0.5.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
