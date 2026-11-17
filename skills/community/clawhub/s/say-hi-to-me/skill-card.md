## Description:

请先说你好.skill provides companion-style greetings, persona management, and opt-in proactive check-in policy for /hi commands and natural conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justzerox](https://clawhub.ai/user/justzerox)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add a bilingual companion interaction layer for greetings, emotional check-ins, digital persona creation, and controlled proactive outreach. Host applications can pair it with OpenClaw Heartbeat or Cron when users explicitly enable scheduled check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proactive check-ins can persist future outreach behavior or surprise users if enabled without clear consent.

Mitigation: Keep proactive mode off by default, require explicit opt-in, respect quiet hours, pause windows, and cooldowns, and review the generated Heartbeat or Cron configuration before use.

Risk: Heartbeat integration can overwrite a workspace HEARTBEAT.md file.

Mitigation: Back up any existing HEARTBEAT.md, verify the target workspace path and environment variables, and review the generated file before deployment.

Risk: Companion personas can overstep emotional or romantic boundaries.

Mitigation: Require explicit activation confirmation for persona changes, especially romantic labels, and enforce the safety policy against dependency-inducing or non-consensual intimacy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justzerox/skills/say-hi-to-me)
- [Runtime Core](references/runtime-core.md)
- [Command Spec](references/command-spec.md)
- [Safety Policy](references/safety-policy.md)
- [Proactive Scheduling](references/proactive-scheduling.md)
- [OpenClaw Heartbeat Integration](references/openclaw-heartbeat-integration.md)
- [Rolecard Structure](references/rolecard-structure.md)
- [Luoshui v1 Persona Template](references/presets/luoshui-v1.yaml)
- [OpenClaw Heartbeat documentation](https://docs.openclaw.ai/heartbeat)
- [OpenClaw Cron documentation](https://docs.openclaw.ai/cron/)
- [OpenClaw message documentation](https://docs.openclaw.ai/message/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Concise natural-language replies, Markdown previews, JSON or script outputs, YAML rolecards, and shell commands for helper workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first bilingual companion responses; proactive delivery requires host Heartbeat or Cron invocation.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
