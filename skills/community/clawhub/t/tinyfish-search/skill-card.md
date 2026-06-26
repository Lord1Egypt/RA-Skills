## Description: <br>
Run web searches via TinyFish Search API and get structured JSON results (title, snippet, URL) ready for LLM consumption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bunsdev](https://clawhub.ai/user/bunsdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve fresh web search results from TinyFish in a structured JSON shape that can be cited, opened, or passed to downstream reasoning. It supports optional country and language targeting for localized searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and API requests are sent to TinyFish, and the skill requires a sensitive API key in the agent environment. <br>
Mitigation: Install only when TinyFish is trusted for the intended queries, store TINYFISH_API_KEY in the host's secret management mechanism, and avoid placing the key in prompts, logs, or shared files. <br>
Risk: The helper script performs network calls through curl, so hosts need visibility into outbound network behavior. <br>
Mitigation: Expose the skill's network and shell/curl behavior in permissions metadata and review the command before execution in restricted environments. <br>


## Reference(s): <br>
- [TinyFish Search API documentation](https://docs.tinyfish.ai/search-api) <br>
- [Tinyfish Search on ClawHub](https://clawhub.ai/bunsdev/tinyfish-search) <br>
- [TinyFish API keys](https://agent.tinyfish.ai/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with bash examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TINYFISH_API_KEY and supports optional location and language query parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
