## Description: <br>
WhenToMeet group scheduling via public REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felixwortmann](https://clawhub.ai/user/felixwortmann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, list, inspect, and delete WhenToMeet scheduling events through the authenticated public REST API. It also guides access to bookings, calendar connections, and event analytics where the API key permits it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use a WhenToMeet API key with access to private scheduling, participant availability, bookings, and connected calendar account metadata. <br>
Mitigation: Install only when this API access is intended, keep API keys secret, and treat scheduling and calendar data as private. <br>
Risk: Some documented actions can delete events, cancel bookings, or expose account and calendar details. <br>
Mitigation: Require explicit user confirmation before destructive actions or before showing account, calendar, booking, or participant metadata. <br>
Risk: Requests may be rejected or throttled when the API key is missing, invalid, lacks permissions, or exceeds rate limits. <br>
Mitigation: Handle documented HTTP errors and rate-limit headers, and avoid retry loops that could consume quota. <br>


## Reference(s): <br>
- [WhenToMeet API Reference](references/API_REFERENCE.md) <br>
- [WhenToMeet OpenAPI Specification](https://whentomeet.io/api/openapi.json) <br>
- [WhenToMeet API Documentation](https://docs.whentomeet.io/api-docs) <br>
- [WhenToMeet Skill Page](https://clawhub.ai/felixwortmann/whentomeet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Bearer API-key authentication and plain JSON request and response bodies.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
