## Description:

Generates printable quality management record forms for field inspection, testing, and equipment checks as Excel and Word templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality teams, field inspectors, test engineers, and equipment maintainers use this skill to create standardized blank inspection records, test report forms, and check sheets that can be printed, filled, signed, and archived.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated .xlsx or .docx files may be written to an unintended or sensitive working directory, or may overwrite existing work.

Mitigation: Choose the working directory intentionally and check for existing files before generation.

Risk: The inspected package references a build script that is not included in the artifact, so document generation may fail in runtimes that do not provide it separately.

Mitigation: Confirm the runtime includes the required generation script before relying on the skill for production form creation.

Risk: Incomplete source details can lead to forms with placeholder standards, sampling plans, or requirements.

Mitigation: Have a qualified user confirm standards, inspection items, sampling plans, and any fields marked for enterprise completion before release.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/duding-engicool/skill-qms-form-builder)
- [ClawHub skill listing](https://clawhub.ai/duding-engicool/skills/skill-qms-form-builder)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [Excel (.xlsx) and Word (.docx) templates with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Templates include blank data rows, dropdown result fields, signature sections, and print-oriented layout; outputs are written to the agent's current working directory.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
