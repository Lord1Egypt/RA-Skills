## Description:

Automate common Word/WPS document operations on Windows via COM, including reading text, replacement, insertion, headings, headers and footers, page breaks, merging, splitting, exporting to PDF or TXT, and adding or replacing images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation users use this skill to run single-document Word or WPS Writer operations on Windows from command-line Python scripts. It is suited for trusted document editing, conversion, and content manipulation workflows that require Microsoft Word or WPS Writer COM automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening Word or WPS documents through COM can expose the user to active-content risks when documents are untrusted.

Mitigation: Use the skill only with trusted documents, or enforce Office/WPS macro and Protected View policies before opening unknown files.

Risk: Write, merge, split, export, and image operations can alter documents or create unexpected outputs.

Mitigation: Use separate output paths, keep backups of source documents, and review generated files before relying on them.

Risk: The required pywin32 dependency is not pinned in the artifact guidance.

Mitigation: Pin and review the pywin32 package version before installing it in a managed environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file-operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for running a bundled Python script; script operations may read, modify, merge, split, export, or create document files.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
