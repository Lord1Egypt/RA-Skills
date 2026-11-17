## Description:

CLI tool for generating tests, scanning contracts, managing story-based tests, and setting up MCP integration in web projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianderrington](https://clawhub.ai/user/ianderrington)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run the Supernal Interface CLI for web project test generation, route and component contract scanning, story-based testing, validation, and MCP setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global installation and setup commands can persistently change project, IDE, MCP, and agent configuration.

Mitigation: Review before installing, use an isolated project or version-controlled checkout first, prefer dry-run or scan-only modes, and pin or verify the npm package version before global installation.

Risk: Commands such as --force, --inject, --migrate, --git-commit, --skip-test, setup-mcp, and setup-claude can make broad or hard-to-review changes when used unintentionally.

Mitigation: Avoid these options unless the change is specifically intended, review resulting diffs and configuration files, and validate generated contracts and tests before merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ianderrington/skills/si)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation or validation of project files, tests, contracts, MCP configuration, and agent integration artifacts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
