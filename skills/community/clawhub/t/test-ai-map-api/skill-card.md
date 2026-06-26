## Description: <br>
Baidu Maps Agent Plan helper for place search, directions, geocoding, reverse geocoding, and weather requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxf969175364](https://clawhub.ai/user/zxf969175364) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to guide agents in making authenticated Baidu Maps Agent Plan requests for map search, route planning, address lookup, reverse geocoding, and weather lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches, addresses, route requests, and precise coordinates are sent to Baidu Maps. <br>
Mitigation: Avoid submitting sensitive home, work, or travel details unless needed for the task. <br>
Risk: The skill uses a Baidu API token for authenticated requests. <br>
Mitigation: Use a scoped or revocable token and pass it through the BAIDU_MAP_AUTH_TOKEN environment variable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxf969175364/test-ai-map-api) <br>
- [Baidu Maps](https://lbs.baidu.com) <br>
- [Baidu Maps Agent Plan Console](https://lbs.baidu.com/apiconsole/agentplan) <br>
- [Baidu Maps API Base URL](https://api.map.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with inline curl commands and parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and the BAIDU_MAP_AUTH_TOKEN environment variable for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
