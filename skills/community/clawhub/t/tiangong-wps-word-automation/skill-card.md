## Description:

Automate common Word/WPS document operations on Windows via COM, including reading text, replacing or inserting content, formatting headings, editing headers and footers, adding page breaks, merging, splitting, exporting, and adding images for single-document workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fadeloo](https://clawhub.ai/user/fadeloo)

### License/Terms of Use:


## Use Case:

Developers and document automation users use this skill to generate command-line actions for Microsoft Word or WPS Writer documents on Windows. It is suited to deliberate single-document operations such as text extraction, edits, page manipulation, merging, splitting, export, and image insertion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document edits and exports can overwrite or modify files at user-selected paths.

Mitigation: Use intentional input and output paths, and prefer saving to new filenames or a dedicated output folder for edit, merge, split, and export commands.

Risk: Exported, split, or merged derivatives may contain the same sensitive content as the source document.

Mitigation: Treat generated DOCX, PDF, and TXT files with the same confidentiality controls as the original document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fadeloo/skills/tiangong-wps-word-automation)
- [Skill documentation](artifact/SKILL.md)
- [Automation script](artifact/scripts/wps_word_automation.py)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can read document text, save edited DOCX files, export PDF or TXT files, and create split or merged document outputs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
