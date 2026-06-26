## Description: <br>
Web search via Tavily API (alternative to Brave). Use when the user asks to search the web / look up sources / find links and Brave web_search is unavailable or undesired. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayegt002](https://clawhub.ai/user/jayegt002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Tavily web searches, retrieve source links, request result counts or images, and apply a local domain blocklist to returned results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the Tavily API key may be sensitive and are sent to an external Tavily service. <br>
Mitigation: Use the skill only when Tavily data sharing is acceptable, and prefer TAVILY_API_KEY or another secret manager over a plaintext apikey file. <br>
Risk: The release has no server-resolved import provenance for this version. <br>
Mitigation: Use a reviewed or pinned source when installing from GitHub. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayegt002/tavily-search-skill) <br>
- [Project homepage](https://github.com/JayeGT002/Tavily-Search-Skill) <br>
- [Tavily API keys](https://app.tavily.com/api-keys) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [Tavily usage API endpoint](https://api.tavily.com/usage) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [JSON search results with quota information, plus shell command guidance for setup and use] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Tavily API key, supports max_results and include_images arguments, and filters configured blocked domains from returned results.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
