## Description: <br>
Searxng Web proxies search queries to a local SearXNG instance and returns normalized JSON search results with titles, URLs, snippets, and sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZomgIrProgrammer](https://clawhub.ai/user/ZomgIrProgrammer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run web searches through a locally hosted SearXNG service and consume concise JSON results inside an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the local SearXNG service configured for the skill. <br>
Mitigation: Install and use this skill only with a trusted SearXNG service, and avoid submitting secrets or highly private text as search queries. <br>
Risk: The skill depends on the availability and behavior of the local SearXNG service. <br>
Mitigation: Verify the local service is running and returning JSON before relying on the skill in an agent workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZomgIrProgrammer/searxng-web) <br>
- [Publisher profile](https://clawhub.ai/user/ZomgIrProgrammer) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON object containing query, count, and results with title, url, snippet, and source fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local SearXNG service at host.docker.internal:8081; count is clamped from 1 to 10.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
