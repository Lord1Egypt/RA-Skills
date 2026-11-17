## Description:

Delegate longer user-facing text generation to Upstage Solar Pro3 while keeping the primary model for planning and tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstage-deployment](https://clawhub.ai/user/upstage-deployment)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to delegate long-form explanations, reports, summaries, and similar user-facing drafts to Upstage Solar Pro3 while keeping planning, reasoning, and tool use with the primary model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long responses may be delegated to OpenRouter or Upstage, including broadly defined session context.

Mitigation: Keep delegation disabled or use a high threshold for confidential work and shared messenger channels, and send only the minimum context needed.

Risk: OpenRouter API key handling guidance is limited.

Mitigation: Store the OpenRouter key in a protected secret mechanism and do not commit or share configuration files containing secrets.

Risk: Delegated text can be forwarded into user-facing channels.

Mitigation: Review delegated output before forwarding it to Slack, Telegram, or other shared channels.

## Reference(s):

- [Solar Delegation Setup Guide](references/setup-guide.md)
- [Upstage Solar Pro3 model reference](https://openrouter.ai/upstage/solar-pro-3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline text, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May pass delegated model output through directly without extra formatting or metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
