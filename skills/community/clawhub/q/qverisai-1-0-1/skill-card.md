## Description: <br>
Search and execute dynamic tools via QVeris API for weather, search, stocks, finance, economics, geolocation, AIGC, news, social media, health data, and other external API-backed tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pippo1980](https://clawhub.ai/user/pippo1980) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill to discover QVeris-hosted tools by capability and execute selected tools with JSON parameters. It is suited for broad API-backed lookups and actions such as weather, finance, search, news, geolocation, social media, AIGC, and health data requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send broad user requests and tool parameters to remote QVeris dynamic tool execution. <br>
Mitigation: Install only if QVeris is an acceptable trust boundary, and require agent confirmation of the selected tool and parameters before execution where possible. <br>
Risk: Requests may include sensitive health, finance, account, or private business data. <br>
Mitigation: Avoid sending secrets or sensitive data through the skill, and use a revocable, least-privilege QVERIS_API_KEY. <br>
Risk: The skill auto-invokes and can execute discovered external tools based on broad prompts. <br>
Mitigation: Review discovered tools, success indicators, and parameters before execution, especially for ambiguous or high-impact requests. <br>


## Reference(s): <br>
- [QVeris](https://qveris.ai) <br>
- [QVeris API endpoint](https://qveris.ai/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/pippo1980/qverisai-1-0-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QVERIS_API_KEY and sends selected requests to QVeris over HTTPS; CLI responses can be formatted for humans or emitted as raw JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
