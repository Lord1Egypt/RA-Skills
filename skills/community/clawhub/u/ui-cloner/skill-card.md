## Description:

Analyzes UI screenshots and generates a reusable .skill file that captures the product's complete design system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenyangze](https://clawhub.ai/user/zhenyangze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to turn one or more authorized UI screenshots from the same product into a reusable design-system skill for recreating similar interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent UI-cloning artifacts and may write generated skills outside the current project if a project directory is not identified.

Mitigation: Keep generated output project-local, review the chosen output path before packaging, and avoid global installation unless explicitly needed.

Risk: UI screenshots may include products or interfaces the user is not authorized to reproduce.

Mitigation: Use only screenshots the user owns or is authorized to clone, and sanitize product names and output paths before packaging.

Risk: Security evidence flags the release as suspicious because packaging and file-writing instructions are under-scoped.

Mitigation: Review the generated files and packaging command before installation or deployment.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/zhenyangze/ui-cloner)
- [ClawHub skill page](https://clawhub.ai/zhenyangze/skills/ui-cloner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown files and shell commands for a generated .skill package]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent project-local or global skill artifacts based on user-provided screenshots and product naming.]

## Skill Version(s):

0.1.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
