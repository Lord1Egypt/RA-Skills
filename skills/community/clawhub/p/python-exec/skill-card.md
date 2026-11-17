## Description:

Python Exec runs local Python snippets through PowerShell, with documented use for creating Word, Excel, and PowerPoint files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[momansouri83](https://clawhub.ai/user/momansouri83)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to execute local Python code for Office document generation when Python 3.10+ and the required document libraries are installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes unrestricted local Python execution beyond its document-creation purpose.

Mitigation: Install only when local Python execution is intended, review the exact code before running it, and use a narrower document-generation skill when only Office file creation is needed.

Risk: Generated code can write files in the local environment.

Mitigation: Run it in a controlled workspace and confirm target file paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/momansouri83/skills/python-exec)

## Skill Output:

**Output Type(s):** [files, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python code snippets and locally written Office document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python 3.10+ and the python-docx, openpyxl, and python-pptx libraries for the documented Office document workflows.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
