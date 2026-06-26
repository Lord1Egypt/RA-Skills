## Description: <br>
Searches the web through the Turing Tavily proxy for real-time information, current events, and other up-to-date data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CAPREaaa](https://clawhub.ai/user/CAPREaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to perform credentialed Tavily web searches through the Turing proxy, including single or batch queries and domain-filtered searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User search queries are sent to the configured Turing Tavily proxy. <br>
Mitigation: Install only when the proxy and TURING_API_BASE are trusted, and do not include secrets, credentials, private documents, or confidential business details in queries. <br>
Risk: The skill uses configured Turing credentials to call the search proxy. <br>
Mitigation: Use a scoped Turing API key and store TURING_API_KEY, TURING_CLIENT, and TURING_ENVIRONMENT in the configured OpenClaw environment rather than in prompts or shared files. <br>


## Reference(s): <br>
- [Turing Documentation](https://docs.turing.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/CAPREaaa/turing-tavily-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON object containing search results and an optional generated answer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include title, URL, content snippet, and publication date when available; supports result limits, page token caps, and domain filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
