## Description:

Guides agents using vx to manage development tools, run project commands, and configure MCP servers and CI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to run vx-managed tools and apply vx configuration patterns in local projects, MCP integrations, and CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatically installed tools, MCP packages, CI actions, and container images may introduce supply-chain risk.

Mitigation: Review dependencies and pin package versions, action refs, and container tags for production use.

Risk: GitHub tokens used by MCP servers or CI can be exposed if placed in tracked configuration.

Mitigation: Keep tokens in secret stores or injected environment variables, not tracked files.

Risk: Applying vx-specific Git and GitHub command guidance outside vx-managed projects may be inappropriate.

Mitigation: Check the project context before routing Git or GitHub operations through vx.

## Reference(s):

- [vx-usage on ClawHub](https://clawhub.ai/loonghao/skills/vx-usage)
- [vx managed command shim guide](https://github.com/vx-org/vx/blob/main/docs/guide/managed-command-shims.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.23 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
