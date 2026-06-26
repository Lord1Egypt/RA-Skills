## Description: <br>
Runrelay helps agents search and book flights, hotels, and travel through the RunRelay API, including low-cost carrier coverage and MCP-compatible workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runrelay](https://clawhub.ai/user/runrelay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, travel agents, and concierge-style agents use this skill to search flights and hotels, compare travel options, and initiate flight bookings through RunRelay services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send passenger details to external services and human operators during travel lookup or booking flows. <br>
Mitigation: Require the agent to show exactly what passenger data will be sent and obtain explicit user confirmation before any external lookup using personal details or any booking action. <br>


## Reference(s): <br>
- [Runrelay ClawHub page](https://clawhub.ai/runrelay/runrelay) <br>
- [RunRelay app](https://app.runrelay.io) <br>
- [RunRelay API base URL](https://api.runrelay.io) <br>
- [RunRelay hotel search endpoint](https://runrelay-hotels.fly.dev/api/search-hotels) <br>
- [Prefy orchestration endpoint](https://prefy.com/api/v1/orchestrate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API endpoint descriptions and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external API calls that require a RUNRELAY_API_KEY and explicit user confirmation before sending passenger details or booking travel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
