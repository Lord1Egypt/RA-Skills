## Description:

Manages shadcn components and projects, including adding, searching, fixing, debugging, styling, and composing UI with project context, component documentation, and usage examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lumacoder](https://clawhub.ai/user/lumacoder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistants use this skill to build and maintain shadcn/ui interfaces in React, Next.js, Vite, and related projects while following component, styling, form, icon, CLI, and registry workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to use unpinned shadcn CLI commands such as npx shadcn@latest.

Mitigation: Pin shadcn to a reviewed version and require explicit approval before running CLI commands that change a project.

Risk: Adding community, URL, or private registry items can install remote code into a project.

Mitigation: Use dry-run, view, or diff before installation, inspect generated files, and approve only trusted registries.

Risk: Private registry tokens could be exposed to endpoints that are not fully trusted.

Mitigation: Configure private registry credentials only for trusted endpoints and avoid sharing tokens with unverified registries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lumacoder/skills/shadcn-ui-skills)
- [shadcn/ui documentation](https://ui.shadcn.com)
- [Skill definition](artifact/SKILL.md)
- [CLI reference](artifact/cli.md)
- [MCP server reference](artifact/mcp.md)
- [Customization and theming](artifact/customization.md)
- [Composition rules](artifact/rules/composition.md)
- [Forms and inputs rules](artifact/rules/forms.md)
- [Icons rules](artifact/rules/icons.md)
- [Styling rules](artifact/rules/styling.md)
- [Base vs Radix rules](artifact/rules/base-vs-radix.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline TypeScript, CSS, JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run shadcn CLI commands; component installs should be previewed with dry-run, diff, or view before applying changes.]

## Skill Version(s):

0.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
