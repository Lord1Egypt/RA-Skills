## Description:

WorkboardSkill guides agents and operators through OpenClaw Workboard card management, including listing, creating, inspecting, dispatching, lifecycle diagnosis, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeanbai0818-cloud](https://clawhub.ai/user/jeanbai0818-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent maintainers use this skill to operate OpenClaw Workboard cards through the CLI, supported slash commands, and lifecycle diagnostics. It helps them manage local board state, dispatch ready cards to worker agents, and understand card status transitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-capable commands can create, dispatch, archive, delete, or bulk modify local Workboard and Gateway state.

Mitigation: Confirm the target board, card, and permission scope before running write-capable commands.

Risk: Dispatch can affect card lifecycle state and may fall back to data-only behavior when Gateway is unavailable.

Mitigation: Check Gateway status and review dispatch output before assuming worker agents started.

Risk: The guide is primarily Chinese-language documentation.

Mitigation: Install it only for users and agents that can accurately follow the Chinese operational guidance.

## Reference(s):

- [Workboard Agent Tool Protocol](references/agent-tools.md)
- [Workboard Card Lifecycle](references/card-lifecycle.md)
- [OpenClaw Workboard documentation](https://docs.openclaw.ai/zh-CN/plugins/workboard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that read or change local OpenClaw Workboard state when executed by an agent or operator.]

## Skill Version(s):

2026.7.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
