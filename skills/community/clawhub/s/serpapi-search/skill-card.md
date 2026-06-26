## Description: <br>
Search Google via SerpAPI (Google Search, Google News, Google Local). Use when you need to search the web, find news articles, or look up local businesses. Supports country/language targeting for region-specific results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericsantos](https://clawhub.ai/user/ericsantos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to run Google Search, Google News, and Google Local queries through SerpAPI with country, language, location, and result-count options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs access to a SerpAPI API key. <br>
Mitigation: Provide the key through an environment variable or managed secret store, keep any local key file permissions restrictive, and rotate the key if trust changes. <br>
Risk: Search terms are sent to SerpAPI and may include sensitive information. <br>
Mitigation: Avoid entering confidential or regulated data in search queries and review organizational policy before use. <br>
Risk: SerpAPI usage may affect account billing or quotas. <br>
Mitigation: Monitor SerpAPI usage and billing for the account tied to the configured API key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericsantos/serpapi-search) <br>
- [SerpAPI search endpoint](https://serpapi.com/search.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Formatted text search results by default, or raw JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, and a SERPAPI_API_KEY secret or local SerpAPI API key file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
