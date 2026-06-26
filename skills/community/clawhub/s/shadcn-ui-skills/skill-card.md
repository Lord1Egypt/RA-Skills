## Description: <br>
Manages shadcn/ui components and projects, including adding, searching, fixing, debugging, styling, and composing UI with project context, component docs, and usage examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lumacoder](https://clawhub.ai/user/lumacoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, update, debug, and review shadcn/ui interfaces while following documented component, styling, form, icon, registry, and CLI practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Adding or updating shadcn/ui components can overwrite or unintentionally change project files. <br>
Mitigation: Review dry-run and diff output before applying component changes, and require explicit approval before overwrite or force operations. <br>
Risk: Community or custom registries can supply untrusted component code or configuration. <br>
Mitigation: Use trusted registries, inspect added files after installation, and validate imports, dependencies, and component composition before keeping the changes. <br>
Risk: Registry authentication tokens can be exposed if configured for untrusted or non-HTTPS endpoints. <br>
Mitigation: Configure registry tokens only for trusted HTTPS endpoints and keep credentials in environment variables or approved secret stores. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lumacoder/shadcn-ui-skills) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [shadcn CLI reference](artifact/cli.md) <br>
- [shadcn MCP server reference](artifact/mcp.md) <br>
- [Customization and theming reference](artifact/customization.md) <br>
- [shadcn/ui documentation](https://ui.shadcn.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, TSX, CSS, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run shadcn CLI commands and may modify project component, theme, and configuration files when the hosting agent has file-system access.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
