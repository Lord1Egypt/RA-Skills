## Description:

MiniMax PDF helps agents create visually polished PDFs, fill PDF form fields, and reformat existing documents using a token-based design system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhlorra](https://clawhub.ai/user/yhlorra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-focused agents use this skill to generate print-ready PDFs, complete existing PDF form fields, or restyle Markdown, text, PDF, or JSON content into a designed PDF.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the skill can automatically install unpinned software.

Mitigation: Review before installing, preinstall pinned dependencies yourself, and avoid the auto-fix path.

Risk: The release evidence reports that PDF rendering may use unrestricted remote or local resources.

Mitigation: Use trusted input files and cover metadata only, and do not allow untrusted remote image URLs or file:// image paths.

Risk: The server security verdict is suspicious.

Mitigation: Run the skill only in an isolated environment with trusted input files until the security findings are reviewed.

## Reference(s):

- [MiniMax PDF on ClawHub](https://clawhub.ai/yhlorra/skills/yh-minimax-pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration; generated artifacts are PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create intermediate HTML, JSON, and PDF files during PDF generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
