## Description: <br>
Configure and troubleshoot OpenClaw Telegram integrations for new bots, DMs, groups, and topic-enabled supergroups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastiangansca](https://clawhub.ai/user/sebastiangansca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Telegram routing for OpenClaw bots, including DMs, groups, topic-enabled supergroups, allowlists, mention gating, and no-reply troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens or chat identifiers could be exposed in shared logs, commits, or screenshots during setup. <br>
Mitigation: Keep bot tokens out of shared logs and commits, redact sensitive identifiers when sharing troubleshooting output, and rotate any exposed token. <br>
Risk: Broad group, webhook, or polling settings could allow unintended replies or duplicate bot processing. <br>
Mitigation: Prefer allowlists and mention gating for groups, review group and webhook settings before enabling them, and keep one active poller or webhook path per bot token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sebastiangansca/telegram-integration-setup) <br>
- [Publisher profile](https://clawhub.ai/user/sebastiangansca) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with configuration checklists and troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable code was found in the release evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
