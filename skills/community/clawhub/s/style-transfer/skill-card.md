## Description:

Extracts a target website's design system and applies it to Vue, React, Next.js, or Tailwind projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[babywhale](https://clawhub.ai/user/babywhale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to transfer a target website's visual system into an existing frontend project. It guides extraction of design tokens, project framework detection, style integration, and build verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow instructs agents to run an unpinned third-party npx package that can download and execute changing code with local privileges.

Mitigation: Use a disposable or version-controlled workspace, pin and review the designlang package before execution, and inspect generated files before importing them.

Risk: Applying extracted design assets can change project styles, Tailwind configuration, HTML font loading, and related frontend files.

Mitigation: Review diffs before accepting changes and run the project's build or development verification commands after integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/babywhale/skills/style-transfer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to project styles, Tailwind configuration, HTML font loading, and verification commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
