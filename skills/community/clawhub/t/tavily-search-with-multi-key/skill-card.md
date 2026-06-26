## Description: <br>
Web search via Tavily API for looking up sources, finding links, and returning concise results with optional short answer summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pazzilivo](https://clawhub.ai/user/Pazzilivo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-backed web searches when Brave web_search is unavailable or undesired. It returns compact search results as JSON, a Brave-like schema, or Markdown for quick source review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Tavily and may contain sensitive information if the agent or user includes it in a query. <br>
Mitigation: Avoid searches containing secrets, private customer data, or sensitive personal information. <br>
Risk: The skill requires a Tavily API key, and multi-key rotation records a small local index under ~/.openclaw/. <br>
Mitigation: Install only when Tavily API key use is acceptable and review local credential and rotation-file handling before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Pazzilivo/tavily-search-with-multi-key) <br>
- [Tavily search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, Brave-compatible JSON, or Markdown search-result lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns title, URL, and snippet/content fields; max results are capped from 1 to 10 and default to 5; optional answer summaries can be included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
