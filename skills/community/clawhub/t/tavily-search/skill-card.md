## Description: <br>
Tavily Search provides AI-agent-focused web search with real-time results, research-style aggregation, image search, citations, and structured responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let an agent query Tavily for current web results, research summaries, image URLs, citations, and JSON-formatted search responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact ships with a bundled Tavily API key in config.json. <br>
Mitigation: Remove or replace the bundled config.json before use, configure your own Tavily API key, and treat any local config file containing the key as a plaintext secret. <br>
Risk: Search queries are sent to Tavily's hosted API and may include sensitive user or business information. <br>
Mitigation: Avoid confidential or regulated queries unless approved for that environment and review privacy expectations before deployment. <br>
Risk: The release has a suspicious security verdict due to credential-handling and privacy disclosure concerns. <br>
Mitigation: Review the skill before installing, scan the artifact, and document credential and query-handling practices for users. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com/) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/tavily-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/paudyyin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text or JSON search results with source URLs, image URLs when requested, and command-line configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search commands call Tavily's hosted API and read a local plaintext config file for the API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
