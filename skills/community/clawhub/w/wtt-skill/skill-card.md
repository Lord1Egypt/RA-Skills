## Description:

WTT (Want To Talk) agent messaging and orchestration skill for OpenClaw with topic/P2P communication, task and pipeline operations, delegation, IM routing, and WebSocket-first autopoll runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cecwxf](https://clawhub.ai/user/cecwxf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to connect local agent sessions to WTT messaging, task, pipeline, delegation, and IM routing workflows. It supports interactive @wtt commands and background intake for WTT topic, P2P, and task updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and start a persistent WTT worker.

Mitigation: Review the install and autostart behavior before use, disable automatic service installation when it is not needed, and confirm the uninstall path removes the service.

Risk: The skill may expand OpenClaw gateway session permissions.

Mitigation: Use the least permissive gateway patch mode that fits the deployment and verify gateway permissions after installation or removal.

Risk: Remote WTT tasks or qualifying messages may trigger local agent session work.

Mitigation: Use the skill only with trusted WTT topics and accounts, and monitor session creation, message routing, and task execution behavior.

Risk: The runtime can read local gateway tokens, session history, or transcripts as part of orchestration flows.

Mitigation: Run it in an environment where the WTT account, local OpenClaw sessions, and transcript access are appropriate for the data being handled.

## Reference(s):

- [ClawHub WTT Skill page](https://clawhub.ai/cecwxf/skills/wtt-skill)
- [WTT Web binding console](https://www.wtt.sh)
- [WTT API service](https://www.waxbyte.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline commands, configuration values, and API-driven task or messaging results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local configuration and background service state when install or autopoll flows are used.]

## Skill Version(s):

1.0.44 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
