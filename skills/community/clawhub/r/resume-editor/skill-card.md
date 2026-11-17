## Description:

Build, edit, and format professional resumes with PDF import, styled HTML/PDF export, and multi-language support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chijiang](https://clawhub.ai/user/chijiang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, import, refine, validate, and export resumes through an AI-assisted local workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editable mode starts a localhost sync server that can write resume changes and can leave sidecar cleanup files.

Mitigation: For sensitive resumes, prefer --no-sync or Copy JSON, stop the sync server after use, and do not share generated editable HTML while the server is running.

Risk: PDF import processes user-provided PDF files through the pinned PyMuPDF dependency.

Mitigation: Avoid untrusted PDFs until the dependency is reviewed or updated.

## Reference(s):

- [Resume Schema](references/resume-schema.json)
- [Data Structure](references/data-structure.md)
- [Customization](references/customization.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/chijiang/skills/resume-editor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON/code file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce local resume JSON, styled HTML, PDF export commands, and theme configuration.]

## Skill Version(s):

1.3.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
