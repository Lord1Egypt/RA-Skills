## Description: <br>
Provides a unified web search and information extraction entry point that routes across content-extraction, Jina Reader, Firecrawl, and web-access CDP to choose an economical toolchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform routed web search, URL extraction, finance lookup, and competitor research with fast, standard, or deep collection modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deep mode can access pages through a logged-in browser session. <br>
Mitigation: Use deep mode only for pages intentionally approved for logged-in access, and avoid private account pages, internal URLs, or token-bearing links. <br>
Risk: Search queries and URLs may be sent to external extraction or search providers. <br>
Mitigation: Avoid submitting confidential queries or sensitive URLs unless external processing has been explicitly approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/halfmoon82/web-intel) <br>
- [Jina Reader endpoint](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON stdout with optional Markdown content fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes selected tool name, result snippets or extracted content, web-access availability, latency, and fallback notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
