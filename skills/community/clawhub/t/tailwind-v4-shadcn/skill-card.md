## Description:

Configures Tailwind v4 with shadcn/ui using a required four-step CSS variable theming architecture for automatic dark mode and common setup-error prevention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and frontend engineers use this skill to configure or migrate React/Vite projects to Tailwind v4 with shadcn/ui, CSS-variable theming, and dark mode support. It also helps debug common Tailwind v4 setup issues such as missing @theme inline mappings, obsolete Tailwind config files, and incorrect animation packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes package-manager commands that execute downloaded tooling and use latest-version installers.

Mitigation: Run setup in a clean working tree, prefer pinned package versions, and review generated dependency and source diffs before committing.

Risk: The setup changes frontend configuration files and may remove older Tailwind configuration that a project still depends on.

Mitigation: Check that the project is a React/Vite Tailwind v4 target, keep a recoverable checkpoint, and adapt the templates to existing project conventions before applying them wholesale.

## Reference(s):

- [Tailwind v4 + shadcn/ui Theming Architecture](references/architecture.md)
- [Migration Guide: Hardcoded Colors to CSS Variables](references/migration-guide.md)
- [Dark Mode Implementation](references/dark-mode.md)
- [Common Gotchas and Solutions](references/common-gotchas.md)
- [Setup Tailwind v4 + shadcn/ui](commands/setup.md)
- [shadcn/ui Tailwind v4 Guide](https://ui.shadcn.com/docs/tailwind-v4)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Theming](https://ui.shadcn.com/docs/theming)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, CSS, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, migration guidance, troubleshooting notes, and reusable frontend configuration templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
