## Description: <br>
Super Search performs multilingual, location-aware web searches with Tavily and Brave, then consolidates results into WhatsApp-formatted summaries with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to answer Portuguese search requests, gather current web results across multiple languages, fetch selected source content, and return a concise WhatsApp-ready response with citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and selected result URLs are sent to Tavily, Brave, and fetched websites. <br>
Mitigation: Use limited-scope API keys and avoid sensitive personal, medical, financial, or confidential searches. <br>
Risk: Local searches default to Sao Lourenco, Minas Gerais, Brazil when no location is supplied. <br>
Mitigation: Ask users for an explicit location when local context matters and state location assumptions in the response. <br>
Risk: Aggregated web results can include incomplete, outdated, or misleading information. <br>
Mitigation: Preserve source links in the response and verify important claims before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runawaydevil/super-search) <br>
- [Tavily search endpoint](https://api.tavily.com/search) <br>
- [Brave Search endpoint](https://api.search.brave.com/res/v1/web/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [WhatsApp-formatted Markdown-like text with source links and optional image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Tavily and Brave API keys for live search execution.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
