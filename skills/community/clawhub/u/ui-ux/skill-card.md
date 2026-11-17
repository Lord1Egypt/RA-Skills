## Description:

Searchable UI/UX design databases with a Python CLI for generating design system recommendations from natural language queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and designers use this skill to choose UI styles, color palettes, typography, UX rules, chart patterns, and stack-specific implementation guidance for websites and applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer commands may resolve the latest package version rather than a fixed release.

Mitigation: Prefer a pinned installer version or a verified artifact before installation.

Risk: Persistence can create Markdown files that future agent sessions may treat as project guidance.

Mitigation: Do not let the agent run --persist automatically; inspect generated Markdown before relying on it.

Risk: Project and page names are used to form persisted output paths.

Mitigation: Use simple project and page names without slashes, dots, or absolute paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/ui-ux)
- [ClawHub publisher profile](https://clawhub.ai/user/wpank)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and generated design-system files when persistence is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally write design-system Markdown files under a project-specific design-system directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
