## Description: <br>
Provides agents with Markdown-formatted search results from a local SearXNG instance for private market, technical, news, and research queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upsurge911-lgtm](https://clawhub.ai/user/upsurge911-lgtm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent builders use this skill to query a local SearXNG service for market intelligence, technical research, real-time briefings, and searches where data sovereignty matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive searches may be logged or forwarded by the configured SearXNG instance or its enabled upstream engines. <br>
Mitigation: Use a trusted local SearXNG instance and review enabled engines, logging, and forwarding behavior before running sensitive queries. <br>
Risk: The skill depends on a local SearXNG service being reachable at http://localhost:8080. <br>
Mitigation: Confirm the service is running and configured before relying on the generated search results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/upsurge911-lgtm/upsurge-searxng) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown search results with titles, source names, URLs, and excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local SearXNG service at http://localhost:8080 and supports category, count, time range, and engine filters.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
