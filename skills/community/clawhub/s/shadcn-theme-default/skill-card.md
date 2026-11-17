## Description:

Enforces the default shadcn/ui Neutral theme (black/white/gray) with OKLCH CSS variables, Tailwind v4 integration, and dark mode support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to apply and maintain the default shadcn/ui Neutral theme, including CSS variables, Tailwind integration, dark mode, and token-based component styling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may change React/TSX files and package dependencies, not just CSS.

Mitigation: Review the planned file list and generated diffs before committing changes.

Risk: Unpinned npm install or npx commands can execute third-party code.

Mitigation: Require approval for package-manager commands and pin package versions where practical.

Risk: Applying the wrong Tailwind theme format can break project styling.

Mitigation: Check the project's Tailwind version before choosing OKLCH/Tailwind v4 or HSL/Tailwind v3 configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guifav/skills/shadcn-theme-default)
- [shadcn/ui configuration schema](https://ui.shadcn.com/schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CSS, TypeScript/TSX, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply edits to CSS, Tailwind configuration, React/TSX files, and package dependencies; review changes before committing.]

## Skill Version(s):

0.1.1 (source: release evidence; artifact claw.json and CHANGELOG.md list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
