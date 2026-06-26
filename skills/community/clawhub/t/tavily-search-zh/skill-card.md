## Description: <br>
Calls Tavily web search through AISA with search depth, topic, and time-range filters for more flexible web retrieval than basic keyword search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need Tavily-backed web search with depth, topic, and recency controls, especially for time-sensitive retrieval tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, URLs, and extracted content may be sent to broader AISA search, extraction, model, and synthesis endpoints than the Tavily-only description clearly discloses. <br>
Mitigation: Avoid confidential queries, private or internal URLs, and sensitive documents unless AISA data handling is acceptable for that content. <br>
Risk: The skill requires a sensitive AISA_API_KEY credential. <br>
Mitigation: Provide the key through a managed environment secret, avoid exposing it in prompts or logs, and rotate it if it is disclosed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/tavily-search-zh) <br>
- [AISA service](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled CLI prints text search results derived from API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; search queries and URLs are sent to AISA endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
