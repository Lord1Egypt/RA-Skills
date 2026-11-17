## Description:

Make your agent 'live beside you' with heartbeats, mood system, relationship evolution, and independent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kitephp](https://clawhub.ai/user/kitephp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add an OpenClaw companion runtime with scheduled heartbeats, mood tracking, relationship state, daily planning, and long-term memory files in a workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent companion behavior and recurring heartbeat jobs can continue updating workspace state after installation.

Mitigation: Require explicit opt-in before enabling cron jobs, document the installed job names, and keep a removal plan for heartbeat and memory-distillation schedules.

Risk: Personal diary, profile, mood, plan, relationship, and memory content may be sent to Anthropic when LLM mode is enabled.

Mitigation: Use a separate workspace and API key, avoid sensitive profile or diary details, and review what local memory files contain before enabling external LLM generation.

Risk: The skill writes long-term memory files and managed blocks into SOUL.md, HEARTBEAT.md, and AGENTS.md.

Mitigation: Review generated managed blocks and keep user-owned content outside the documented block markers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kitephp/skills/soul-agent)
- [soul-layout.md](references/soul-layout.md)
- [managed-blocks.md](references/managed-blocks.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Markdown and text guidance with bash commands; runtime scripts produce JSON state, Markdown memory, and log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update workspace-resident soul profile, state, plan, mood history, life log, memory, and managed bootstrap files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
