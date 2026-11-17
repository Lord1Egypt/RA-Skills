## Description:

Guides agents running in Hermes to use the preconfigured Render MCP server, skip unavailable CLI and setup steps, and adapt upstream Render skills to this environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ojusave](https://clawhub.ai/user/ojusave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when managing Render resources from a Hermes-hosted agent. It tells the agent which Render MCP tools are available, when to ask for workspace or operation confirmation, and when to hand CLI-only tasks back to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad Render MCP access that can change production resources, including deploys, restarts, service updates, environment-variable changes, resource creation, and database writes.

Mitigation: Before allowing mutating actions, require the agent to name the workspace, target resource, exact change, and wait for explicit user confirmation.

Risk: Agents may attempt Render CLI actions even though the CLI is unavailable in the Hermes container.

Mitigation: Use MCP equivalents when available; for CLI-only tasks, draft commands for the user to run locally instead of attempting installation or execution.

Risk: The active Render workspace can be ambiguous in multi-workspace accounts.

Mitigation: List available workspaces and ask the user to choose when more than one plausible workspace exists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ojusave/skills/render-on-hermes)
- [Server-resolved GitHub provenance](https://github.com/ojusave/hermes-render-ms6m0o42/tree/main/skills/render-on-hermes)
- [Render MCP endpoint](https://mcp.render.com/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline tool and command names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment-specific constraints for Render MCP access and unavailable Render CLI behavior.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
