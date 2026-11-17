## Description:

Control and query SwitchBot devices with OpenAPI v1.1, including device status, device commands, scenes, family and room grouping, and AI MindClip recordings, summaries, todos, daily memories, and weekly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[switchbot-dev](https://clawhub.ai/user/switchbot-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to manage SwitchBot smart-home devices, run scenes, and retrieve AI MindClip transcript, summary, todo, and memory data through authenticated OpenAPI calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can unlock doors, open garages, create or delete keypad codes, and execute scenes.

Mitigation: Use only with a SwitchBot account intended for agent control and require explicit confirmation outside the skill before those actions.

Risk: The skill can expose AI MindClip transcripts, summaries, todos, and location memories.

Mitigation: Confirm user intent before displaying recording-derived content and avoid broad shared tokens.

Risk: Shared or overly broad credentials could let an agent affect more devices or data than intended.

Mitigation: Provision narrowly scoped account access where possible and store SwitchBot token and secret values outside logs or hardcoded files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/switchbot-dev/skills/switchbot-cloudapi)
- [SwitchBot OpenAPI Endpoint](https://api.switch-bot.com)
- [Commands Reference](references/commands.md)
- [API Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SwitchBot token and secret environment variables; outputs may include device state and recording-derived personal data.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
