## Description:

Automate common PowerPoint/WPS Presentation operations on Windows via COM, including reading text, notes, and outlines; exporting PDFs and images; replacing text; inserting or deleting slides; unifying font, size, and theme; and extracting images or media for single-presentation actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fadeloo](https://clawhub.ai/user/fadeloo)

### License/Terms of Use:


## Use Case:

Developers, analysts, and productivity users can use this skill to run single-file PowerPoint or WPS Presentation automation tasks on Windows, such as extracting slide content, exporting presentation assets, and applying controlled edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation edit commands can overwrite or materially change local files.

Mitigation: Use explicit output or save paths and keep backups before replace, delete-slide, font, or theme operations.

Risk: Slide text, speaker notes, and exported assets may contain sensitive content that can be written to disk or printed to output.

Mitigation: Avoid exporting notes, slide text, or images from sensitive presentations unless that disclosure and storage location are intended.

Risk: The skill depends on local Windows COM automation and pywin32, so the execution environment affects behavior and trust boundaries.

Mitigation: Install in a normal non-admin Python environment, consider pinning pywin32, and run only on machines with trusted PowerPoint or WPS installations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with command examples, file paths, and generated presentation-related files when commands are executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read, create, export, or modify local presentation, text, PDF, PNG, and image files depending on the selected command.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
