## Description: <br>
AI-powered web search using Tavily API for accurate and relevant results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yshuolu](https://clawhub.ai/user/yshuolu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-backed web searches from a shell command and retrieve a concise answer for a user-supplied query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the Tavily API key are sent to Tavily's search API. <br>
Mitigation: Use a dedicated Tavily API key and avoid sensitive personal data, secrets, or confidential internal terms in searches. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yshuolu/test-search-clone) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API Endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text answer printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and TAVILY_API_KEY; sends the supplied query to Tavily with max_results set to 5 and include_answer enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
