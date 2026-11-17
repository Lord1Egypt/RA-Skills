## Description:

Generates professional resumes as PDF, Word, or HTML from YAML, Markdown, or HTML inputs with multiple templates and Chinese/English support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[31504254](https://clawhub.ai/user/31504254)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate polished resumes and CVs from structured YAML, Markdown, or HTML content, then export them to PDF, DOCX, or print-ready HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML-to-PDF conversion can allow crafted resume HTML to access local files or network resources during rendering.

Mitigation: Convert only trusted HTML, run renderers in an isolated environment, and block local or network resource loading before returning generated PDFs.

Risk: Resume export writes files to user-selected output paths and may create fallback HTML files.

Mitigation: Choose output paths deliberately and review whether an existing file could be overwritten before running export commands.

Risk: Unpinned dependencies and optional PDF backends can change rendering behavior or security posture.

Mitigation: Pin and review dependencies before production use, and select a reviewed PDF backend for deployed workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/31504254/skills/resume-generator-clean)
- [Artifact README](artifact/README.md)
- [ReportLab](https://www.reportlab.com/)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command snippets and generated PDF, DOCX, or HTML resume files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output paths are user-selected; PDF generation may fall back to print-ready HTML when optional PDF backends are unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
