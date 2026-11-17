## Description:

Helps agents build, edit, inspect, and troubleshoot WordPress Elementor sites through the elementor-mcp MCP server, including setup, engine detection, Pro/free workflow selection, design-system work, forms, dynamic data, and recovery guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benkalsky](https://clawhub.ai/user/benkalsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site builders use this skill to connect an agent to an Elementor-enabled WordPress site, choose the correct Elementor Pro/free and classic/atomic workflow, and carry out page-building or editing tasks with verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make real changes to WordPress pages and site configuration.

Mitigation: Use it only on a site intended for agent editing, require explicit user direction for changes, and get backups and approval before production use.

Risk: Setup can store a reusable WordPress application password in .mcp.json.

Mitigation: Use a least-privileged application password, keep .mcp.json out of version control, and revoke the password after handoff.

Risk: Installing or overriding the pinned MCP plugin release can introduce supply-chain risk.

Mitigation: Prefer the default pinned plugin version unless another release is independently verified with an expected SHA-256 digest.

Risk: Leaving MCP authoring plugins active after launch expands the site's edit surface.

Mitigation: Deactivate or remove the MCP authoring plugin after the build or handoff is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benkalsky/skills/siteagent-elementor-studio)
- [elementor-mcp GitHub repository](https://github.com/Digitizers/elementor-mcp)
- [wordpress-api-pro GitHub repository](https://github.com/Digitizers/wordpress-api-pro)
- [Building on Elementor 4 (atomic / V4)](references/atomic-v4.md)
- [Elementor 4 design system CRUD](references/design-system-crud.md)
- [Engine and Premium plugin guidance](references/engine-and-premium.md)
- [Forms reference](references/forms.md)
- [Header / Footer reference](references/header-footer.md)
- [Dynamic data stacks reference](references/dynamic-data.md)
- [Error recovery reference](references/error-recovery.md)
- [Section recipe library](references/recipes.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed MCP tool calls, setup commands, WordPress configuration steps, and verification instructions.]

## Skill Version(s):

1.7.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
