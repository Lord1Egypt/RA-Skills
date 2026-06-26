## Description: <br>
Performs internet searches through a self-hosted SearXNG instance and returns structured web results with titles and URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lokixshrishi](https://clawhub.ai/user/lokixshrishi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill when they need current web search results for news, documentation checks, fact verification, research links, or other time-sensitive information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the configured local SearXNG service and may be logged or forwarded by that service. <br>
Mitigation: Use only a trusted SearXNG instance, and avoid submitting secrets, credentials, private internal data, or sensitive personal information in queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lokixshrishi/search-web) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [JSON array of search results with title and url fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to five results from the configured local SearXNG endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
