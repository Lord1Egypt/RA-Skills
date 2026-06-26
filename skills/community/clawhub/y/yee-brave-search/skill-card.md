## Description: <br>
A custom tool for web searching using Brave Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mryee2023](https://clawhub.ai/user/mryee2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let an agent run Brave Search API web searches and return current search results for user queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Brave Search using the user's API key, which can expose sensitive terms. <br>
Mitigation: Avoid using the skill for secrets, credentials, private documents, or sensitive personal information. <br>
Risk: The release has privacy and permission-disclosure gaps around network and environment-variable requirements. <br>
Mitigation: Confirm BRAVE_API_KEY handling and outbound access to the Brave Search API are approved before deployment. <br>


## Reference(s): <br>
- [Brave Search API web search endpoint](https://api.search.brave.com/res/v1/web/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON array of search results or JSON error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRAVE_API_KEY and outbound network access to Brave Search.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
