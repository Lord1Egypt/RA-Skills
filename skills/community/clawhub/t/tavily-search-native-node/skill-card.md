## Description: <br>
Minimal Tavily web search skill for OpenClaw that runs a native Node.js script to return summarized search results with source citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwestburg](https://clawhub.ai/user/jwestburg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs current web information, recent news, comparison research, or real-time context with citations. It is intended for Tavily-backed web search, not URL scraping or private-data lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Tavily and may disclose sensitive information. <br>
Mitigation: Do not submit secrets, confidential text, client identifiers, hostnames, private incident details, or private strategy unless that disclosure is explicitly approved. <br>
Risk: The skill requires a Tavily API key and can consume Tavily credits. <br>
Mitigation: Provide the key through the process environment, prefer basic-depth searches unless deeper research is needed, and monitor Tavily pricing, limits, and usage. <br>
Risk: Search results and synthesized answers may be incomplete, stale, or wrong. <br>
Mitigation: Review the returned sources before relying on the result, especially for decisions involving current events, money, safety, legal obligations, or operational changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jwestburg/tavily-search-native-node) <br>
- [Tavily app and API key portal](https://app.tavily.com) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON search results, with Markdown and shell-command guidance in the skill instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output includes the searched query, a synthesized answer, result titles, URLs, snippets, and timing; JSON mode returns the Tavily response.] <br>

## Skill Version(s): <br>
1.0.11 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
