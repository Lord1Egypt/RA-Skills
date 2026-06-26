## Description: <br>
TripAI helps agents send natural-language Chinese travel queries to Ctrip's Wendao service for hotels, flights, trains, attractions, day trips, and events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trips-ai](https://clawhub.ai/user/trips-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to translate detailed Chinese travel requests into Ctrip Wendao queries for itinerary, ticket, lodging, attraction, local activity, and event information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel questions are sent to Ctrip's service and may include sensitive itinerary or preference details. <br>
Mitigation: Share only travel information needed for the query and avoid passwords, payment data, or unrelated private information. <br>
Risk: The optional TRIPAI_API_KEY can be exposed if stored carelessly on a shared system. <br>
Mitigation: Prefer a short-lived environment variable for temporary use, or restrict permissions on any local API-key file. <br>


## Reference(s): <br>
- [TripAI on ClawHub](https://clawhub.ai/trips-ai/tripai-skill) <br>
- [Ctrip Wendao OpenClaw](https://www.ctrip.com/wendao/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and Ctrip API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq; TRIPAI_API_KEY is optional but may reduce rate limiting.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
