## Description:

Calls vwu.ai Sihai models through an OpenAI-compatible chat completions interface for the model IDs listed with the skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure a vwu.ai API key and call the listed Sihai models from a shell command. It is suited for workflows that can send prompts to vwu.ai or to a trusted explicitly configured VWU_BASE_URL endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the configured API key are sent to vwu.ai or to the endpoint selected by VWU_BASE_URL.

Mitigation: Install only when that data flow is acceptable, avoid sensitive prompts, and keep the runtime environment controlled.

Risk: A shared shell, CI job, or agent environment could set VWU_BASE_URL to an unexpected endpoint.

Mitigation: Use trusted environments and inspect or pin VWU_BASE_URL before running the command.

## Reference(s):

- [vwu.ai](https://vwu.ai)
- [ClawHub Skill Page](https://clawhub.ai/a3273283/skills/vwu-sihai)
- [Publisher Profile](https://clawhub.ai/user/a3273283)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VWU_API_KEY; optionally uses VWU_BASE_URL to select the endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
