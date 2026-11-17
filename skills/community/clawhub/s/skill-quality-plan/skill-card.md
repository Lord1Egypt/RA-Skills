## Description:

Generates product-specific quality plan documents for general manufacturing, covering quality objectives, control processes, inspection standards, risk assessment, and related modules, with Markdown and HTML output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing quality teams, engineers, and external users use this skill to collect product requirements, confirm a 12-module quality-plan outline, and generate editable Markdown plus print-ready HTML quality plan documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML export can preserve active web code from third-party Markdown content or metadata.

Mitigation: Use trusted inputs, review generated Markdown and metadata before export, and prefer sanitized HTML export or Markdown-only sharing for sensitive quality plans.

Risk: Generated output paths can overwrite existing quality-plan files.

Mitigation: Confirm output filenames and keep backups or versioned paths before exporting final Markdown or HTML.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duding-engicool/skills/skill-quality-plan)
- [Server-Resolved Source Repository](https://github.com/duding-engicool/skill-quality-plan)
- [Publisher Profile](https://clawhub.ai/user/duding-engicool)
- [Quality Plan Outline](references/quality-plan-outline.md)
- [Industry Standards Reference](references/industry-standards.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown quality-plan document with optional HTML export and supporting shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces product-specific documents after user information collection and outline confirmation.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
