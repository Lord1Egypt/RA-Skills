## Description:

Render PDF pages to images, extract embedded images, annotate PDFs, and perform advanced PDF inspection using pymupdf (fitz).

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-ai-tech](https://clawhub.ai/user/maverick-ai-tech)

### License/Terms of Use:


## Use Case:

Developers and document-processing agents use this skill to render PDF pages as image files, extract embedded images, and inspect document page metadata with deterministic PyMuPDF commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local PDF files and can render or extract document content into separate image files.

Mitigation: Use it only with PDFs the agent is authorized to inspect and choose output directories deliberately.

Risk: Exported image filenames are deterministic and may replace same-named prior outputs in a reused directory.

Mitigation: Write to a fresh or task-specific output directory before preserving or sharing generated images.

Risk: The evidence guidance treats this release as a local rendering and extraction helper, not a reviewed redaction or annotation tool.

Mitigation: Do not rely on it for final redaction or annotation workflows without separate review of the resulting PDF handling.

Risk: PyMuPDF is an external dependency installed into the agent environment.

Mitigation: Install PyMuPDF in a virtual environment and pin a reviewed version when used in managed workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-ai-tech/skills/pymupdf)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output may include image files or plain text document metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on local PDF files and writes exported or extracted images to user-selected output directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
