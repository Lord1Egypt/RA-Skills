## Description: <br>
请先说你好.skill provides companion-style greetings, persona management, and optional host-triggered proactive check-ins through /hi commands and natural conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justzerox](https://clawhub.ai/user/justzerox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to start lightweight companion chats, manage digital personas, and configure opt-in proactive check-ins through a host Heartbeat or Cron setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local companion state and may write HEARTBEAT.md when proactive behavior is configured. <br>
Mitigation: Review the workspace location before enabling proactive settings and keep local state files within the intended project or OpenClaw workspace. <br>
Risk: Host-triggered proactive greetings can create unexpected outreach if Heartbeat or Cron is scoped too broadly. <br>
Mitigation: Keep proactive delivery disabled until explicitly needed, then scope the host schedule, active hours, and delivery target before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justzerox/say-hi-to-me) <br>
- [Runtime Core](references/runtime-core.md) <br>
- [Command Spec](references/command-spec.md) <br>
- [Rolecard Structure](references/rolecard-structure.md) <br>
- [Proactive Scheduling](references/proactive-scheduling.md) <br>
- [OpenClaw Heartbeat Integration](references/openclaw-heartbeat-integration.md) <br>
- [Safety Policy](references/safety-policy.md) <br>
- [OpenClaw Heartbeat documentation](https://docs.openclaw.ai/heartbeat) <br>
- [OpenClaw Cron documentation](https://docs.openclaw.ai/cron/) <br>
- [OpenClaw message documentation](https://docs.openclaw.ai/message/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with commands, JSON examples, and generated local configuration or role files when the user confirms changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Replies are concise by default and proactive greetings remain gated by user opt-in and host scheduling.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
