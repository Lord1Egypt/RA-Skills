## Description: <br>
Tavily AI Search API integration for OpenClaw. Provides web search capabilities using Tavily's AI-powered search engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to add Tavily-powered web search to an agent, configure the required API key, and run searches with options for depth, result count, generated answers, and images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Tavily API key is required and could be exposed if copied into shared files, logs, or prompts. <br>
Mitigation: Store the API key privately, prefer environment variables or protected configuration, and avoid including it in prompts or shared examples. <br>
Risk: Search queries are sent to an external search provider. <br>
Mitigation: Avoid sending secrets, regulated data, or confidential internal queries through the Tavily search API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/tavily-search-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, bash, and Python examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tavily API key and the tavily-python package; search queries are sent to Tavily as the external provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
