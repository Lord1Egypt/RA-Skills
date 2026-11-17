## Description:

Zero Token configures an OpenClaw fallback through the Free-Way gateway so an agent can continue on free-tier LLM providers when its primary model fails or token budget is exhausted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtmpss](https://clawhub.ai/user/mtmpss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a local fallback endpoint for OpenClaw so work can continue when a primary model is unavailable or out of tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local fallback gateway can receive fallback prompts and provider API keys.

Mitigation: Use disposable or tightly scoped free-tier keys, review each provider's terms, and avoid confidential workloads unless the gateway and providers have been approved.

Risk: The setup script installs and runs a third-party gateway locally.

Mitigation: Review the pinned Free-Way source and commit before running setup, and keep the gateway bound to localhost unless a separate network review approves broader exposure.

Risk: The bundled SOUL behavior instructions are broad for a fallback utility.

Mitigation: Inspect, narrow, or remove global behavior instructions before deployment if the host agent already has its own behavior, security, or policy controls.

## Reference(s):

- [Zero Token ClawHub listing](https://clawhub.ai/mtmpss/skills/zero-token)
- [Zero Token homepage](https://github.com/mtmpss/zero-token)
- [Free-Way gateway](https://github.com/GoDiao/Free-Way)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [I-Lang protocol](https://ilang.ai)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configures a local fallback gateway and provider keys outside the skill card generation flow.]

## Skill Version(s):

1.0.7 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
