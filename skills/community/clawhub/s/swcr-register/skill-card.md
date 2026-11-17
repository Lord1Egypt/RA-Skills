## Description:

Swcr Register helps prepare Chinese software copyright registration materials by generating source-code identification documents, operation manuals, filing information, and optional guided form-filling support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiongdi666](https://clawhub.ai/user/daxiongdi666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software publishers use this skill to prepare materials for Chinese computer software copyright registration, including source-code documentation, a software operation manual, and filing-information notes. It can also guide online form filling when the user explicitly confirms each step.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can read broad project contents while preparing source-code documentation.

Mitigation: Run it only on trusted repositories and choose an output folder that does not expose unrelated private files.

Risk: Symlinks or unexpected paths in the target repository could expose private locations.

Mitigation: Avoid running it on directories that contain symlinks to sensitive locations, and review the selected source directory before generation.

Risk: Generated registration text may be inaccurate or incomplete for a filing.

Mitigation: Manually review generated function descriptions, technical descriptions, identity materials, addresses, uploads, and every browser step before any submission.

## Reference(s):

- [WiseFlow repository](https://github.com/TeamWiseFlow/wiseflow)
- [Swcr Register on ClawHub](https://clawhub.ai/daxiongdi666/skills/swcr-register)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Guidance]

**Output Format:** [DOCX files, Markdown filing notes, and concise instructions with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates source-code document, operation manual, and filing-information files; optional browser-assisted filing requires explicit user confirmation and manual review before submission.]

## Skill Version(s):

1.5.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
