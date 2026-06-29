## Description: <br>
A web research and discovery skill that routes agent requests to tools for search, page crawling, package and repository lookup, API documentation retrieval, structured extraction, comparison, and service-status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and other external users use this skill to gather current web information, inspect packages and repositories, retrieve API documentation, extract structured data from pages, compare technologies, troubleshoot errors, and check service health through the XiaoBenYang web research service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, URLs, reasoning fields, and fetched content may be sent to an external XiaoBenYang service. <br>
Mitigation: Avoid sending credentials, private code, internal URLs, personal data, or other sensitive material through the skill. <br>
Risk: The XBY API key is stored in a local .env file when configured. <br>
Mitigation: Treat the API key as a secret, limit local file access, exclude .env from sharing, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cainingnk/xby-web-research-assistant) <br>
- [XiaoBenYang service](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with structured tool results from API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY and may return raw JSON-like results for the agent to summarize.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
