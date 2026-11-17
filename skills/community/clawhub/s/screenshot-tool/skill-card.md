## Description:

Captures full-page webpages and converts PPT, Word, Excel, and PDF documents into high-resolution PNG images while preserving layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[834948655](https://clawhub.ai/user/834948655)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture webpages or convert presentation, document, spreadsheet, and PDF files into PNG screenshots for review, sharing, or downstream visual workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted URLs, filenames, or output paths could cause unintended local commands to run.

Mitigation: Run the skill in a constrained environment and avoid untrusted URLs, filenames, and output paths until command inputs are validated and safely executed.

Risk: The documented setup uses global npm and pip installs plus sudo package installation.

Mitigation: Review installation commands before use and prefer a disposable container or managed environment instead of a primary workstation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/834948655/skills/screenshot-tool)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; generated artifacts are PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses agent-browser for webpage screenshots and LibreOffice, poppler-utils, pdf2image, and Pillow for document conversion.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
