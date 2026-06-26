## Description: <br>
AI-powered presentation generation using 2slides API. Create slides from text content, match reference image styles, or summarize documents into presentations. Use when users request to "create a presentation", "make slides", "generate a deck", "create slides from this content/document/image", or any presentation creation task. Supports theme selection, multiple languages, and both synchronous and asynchronous generation modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to generate presentation decks from text, documents, or reference images through the 2slides API. It also helps search presentation themes and check asynchronous generation jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation text, document-derived summaries, and reference images are sent to the 2slides API for processing. <br>
Mitigation: Avoid confidential, regulated, or sensitive content unless the user has approval to process it with 2slides. <br>
Risk: API keys can be exposed through URLs, logs, screenshots, shared configuration, or shell history. <br>
Mitigation: Prefer environment-variable-based script usage or secure MCP configuration, and rotate the key if it may have been exposed. <br>
Risk: Generated decks may omit nuance or misrepresent source documents when long content is summarized. <br>
Mitigation: Review generated slides against the original source material before publication or customer-facing use. <br>


## Reference(s): <br>
- [2slides API Reference](references/api-reference.md) <br>
- [2slides MCP Integration Guide](references/mcp-integration.md) <br>
- [2slides API Portal](https://2slides.com/api) <br>
- [2slides Website](https://2slides.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 2slides slide URLs, PDF URLs, job IDs, theme search results, and MCP configuration guidance when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
