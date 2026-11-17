## Description:

Generate practical UI design systems and starter pages using local style/color/typography datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:

MIT

## Use Case:

Developers and design-focused agents use this skill to select UI style, color, typography, and layout patterns for landing pages or dashboards, then produce buildable design specs and starter HTML/CSS when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented PowerShell helper uses ExecutionPolicy Bypass, and the server security summary says the helper script is missing from the artifact.

Mitigation: Review before installation, and do not run the helper unless the actual script is included, reviewed, and invoked from a trusted package path without ExecutionPolicy Bypass.

Risk: Generated starter UI files may be treated as production-ready without confirming accessibility and token application.

Mitigation: Review generated files, verify WCAG-oriented contrast, confirm stylesheet references, and check that selected style, color, and typography tokens are reflected in CSS variables.

## Reference(s):

- [Ui Design Optimizer on ClawHub](https://clawhub.ai/dalomeve/skills/ui-design-optimizer)
- [Dalomeve publisher profile](https://clawhub.ai/user/dalomeve)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown design specification with optional HTML/CSS starter files and file-path evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected dataset row slugs, design tokens, interaction rules, and verification notes.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
