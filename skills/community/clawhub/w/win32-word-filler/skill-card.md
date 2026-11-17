## Description:

Fill and edit Word .docx templates on Windows using Microsoft Word automation to preserve formatting, images, underlines, page breaks, and table layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winezzz999](https://clawhub.ai/user/winezzz999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation agents use this skill to fill or edit local Word templates on Windows while keeping the original document layout intact. It is best suited for structured reports, cover fields, table answers, page breaks, and targeted find-and-replace operations in .docx files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Word automation acts on local .docx files and depends on a Windows machine with Microsoft Word installed.

Mitigation: Run it only on trusted local documents in a compatible Windows environment and review the output document before sharing it.

Risk: The documented debug step can force-close every running Word process.

Mitigation: Avoid the `taskkill /f /im WINWORD.EXE` debug command unless all Word documents are saved and you intentionally want to close every Word process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/winezzz999/skills/win32-word-filler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples and Python CLI usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance and commands for local .docx template filling; generated documents are written by the bundled CLI when run in a compatible Windows environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
