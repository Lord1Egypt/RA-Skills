## Description:

AI-powered presentation generation using the 2slides API for creating slides from text, matching reference image styles, or summarizing documents into presentations with theme selection, multiple languages, and synchronous or asynchronous generation modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to turn text, outlines, documents, or reference-image style prompts into generated slide decks through the 2slides API. It also supports theme discovery, async job polling, multilingual generation, and optional MCP-based access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation text, document summaries, and reference image URLs are sent to 2slides for processing.

Mitigation: Avoid confidential, regulated, or private documents unless the user has permission and accepts processing by 2slides.

Risk: API keys may be exposed through shell configuration files or shared MCP configuration.

Mitigation: Prefer environment variables for direct scripts, protect shell configuration files, and do not share MCP configuration containing credentials.

Risk: Using the local 2slides MCP package adds dependency and package-source risk.

Mitigation: Pin or review the 2slides-mcp package before enabling it locally.

## Reference(s):

- [2slides API Reference](references/api-reference.md)
- [MCP Integration Guide](references/mcp-integration.md)
- [2slides API Portal](https://2slides.com/api)
- [2slides Website](https://2slides.com)
- [2slides MCP GitHub Repository](https://github.com/2slides/mcp-2slides)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces links to generated online slides, downloadable PDFs, theme search results, or async job status when API calls complete.]

## Skill Version(s):

1.0.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
