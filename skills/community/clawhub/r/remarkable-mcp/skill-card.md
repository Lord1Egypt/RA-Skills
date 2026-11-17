## Description:

Access reMarkable tablet documents, notebooks, PDFs, and EPUBs for reading, browsing, searching, text extraction, OCR, annotations, highlights, and page rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sammorrowdrums](https://clawhub.ai/user/sammorrowdrums)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to connect OpenClaw to a user's reMarkable tablet so they can browse documents, search notes, extract text, render pages, and inspect recent tablet content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an external MCP server access to private tablet documents and credentials.

Mitigation: Review the skill before installing and only grant tablet or credential access in environments where that exposure is acceptable.

Risk: Cloud and OCR modes may involve third-party processing of sensitive notes.

Mitigation: Prefer USB mode for sensitive content and use cloud or OCR modes only after accepting the privacy implications.

Risk: The setup runs the `remarkable-mcp` package without a pinned version in the artifact examples.

Mitigation: Pin or verify the package before running it with tablet access or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sammorrowdrums/skills/remarkable-mcp)
- [Publisher profile](https://clawhub.ai/user/sammorrowdrums)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with JSON configuration examples and MCP tool output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide setup for USB, SSH, cloud, and OCR modes; MCP tools may return extracted text, search results, document metadata, and rendered page images.]

## Skill Version(s):

0.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
