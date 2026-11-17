## Description:

Formats Word documents and generates PDFs according to Shuke company printing requirements, including prescribed Chinese fonts, margins, line spacing, and page grid settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[an0027](https://clawhub.ai/user/an0027)

### License/Terms of Use:

MIT-0

## Use Case:

External users and document automation practitioners use this skill to format DOCX files, generate compliant PDFs, batch-convert document folders, and verify required font usage for Shuke-style print documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: System-wide font installation can modify local font directories or require elevated privileges.

Mitigation: Review font files and their source directory before installation, and avoid running the installer with sudo unless the environment and files are trusted.

Risk: PDF conversion can process local document content and may touch local or network resources.

Mitigation: Convert only trusted DOCX files, and use a sandboxed or offline conversion environment for untrusted documents.

Risk: Generated debug HTML may contain sensitive document content.

Mitigation: Delete generated debug HTML after review or restrict access to the output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/an0027/skills/shuke-document-formatting)
- [OpenClaw issue tracker](https://github.com/openclaw/openclaw/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples and generated DOCX, PDF, font report, or debug HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on local fonts, document conversion tools, and trusted input DOCX files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
