## Description: <br>
Access reMarkable tablet documents, notebooks, PDFs, and EPUBs for reading, browsing, searching, text extraction, handwriting OCR, annotations, highlights, and page rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SamMorrowDrums](https://clawhub.ai/user/SamMorrowDrums) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to their reMarkable tablet so it can browse, search, read, and extract content from notebooks, PDFs, EPUBs, annotations, highlights, and rendered pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud mode and OCR can expose document content to external services. <br>
Mitigation: Prefer USB mode for sensitive documents and enable cloud mode or Google Vision OCR only when that processing is acceptable. <br>
Risk: Tokens and API keys may be placed in local MCP configuration. <br>
Mitigation: Keep REMARKABLE_TOKEN and GOOGLE_VISION_API_KEY out of shared configs and rotate or remove credentials when access is no longer needed. <br>
Risk: Leaving the MCP server configured may continue to allow agent access to tablet documents. <br>
Mitigation: Remove the MCP entry when agent access to reMarkable documents is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SamMorrowDrums/remarkable-mcp) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/SamMorrowDrums) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, images] <br>
**Output Format:** [Markdown guidance with JSON configuration examples; MCP tool responses can include document text, search results, metadata, and PNG/SVG page renders.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports USB, SSH, and cloud connection modes; OCR requires a Google Vision API key.] <br>

## Skill Version(s): <br>
0.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
