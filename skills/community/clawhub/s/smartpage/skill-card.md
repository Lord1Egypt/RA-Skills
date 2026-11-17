## Description:

Auto-fit Markdown to one A4 page. Binary search optimal font size, render with 10 themes, export PDF+PNG+MD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxjhello](https://clawhub.ai/user/fxjhello)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use SmartPage to format Markdown or converted document content onto a single A4 page and export PDF, PNG, and Markdown files with selectable themes and layout controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run mutable third-party code with broad local effects.

Mitigation: Review the skill before installing, use a disposable or restricted workspace, and inspect and pin the upstream code before running npm install.

Risk: Document formatting can expose sensitive input files or generated outputs through temporary and output locations.

Mitigation: Avoid sensitive documents unless the temp and output locations are controlled.

Risk: The optional web editor starts a local development server.

Mitigation: Stop the dev server when editing is finished.

## Reference(s):

- [SmartPage on ClawHub](https://clawhub.ai/fxjhello/skills/smartpage)
- [fxjhello publisher profile](https://clawhub.ai/user/fxjhello)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and CLI options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for PDF, PNG, and Markdown document exports through the referenced SmartPage CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
