## Description: <br>
Search award flight availability across 24 mileage programs, including business and first class, with detailed route and booking info via the seats.aero API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JarrodJS](https://clawhub.ai/user/JarrodJS) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travelers, points users, and travel-planning agents use this skill to search seats.aero award availability by route, mileage program, cabin, and date range, then inspect trip details and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a seats.aero API key and instructs the agent to keep it available during the conversation. <br>
Mitigation: Use a revocable API key, avoid exposing it in screenshots or logs, and rotate it if it may have appeared in chat history. <br>
Risk: Cached award availability can become stale before booking. <br>
Mitigation: Check the reported freshness timestamp and verify availability with the booking program before relying on results. <br>


## Reference(s): <br>
- [Seats.aero Partner API access](https://seats.aero/partner) <br>
- [Seats.aero Partner API base endpoint](https://seats.aero/partnerapi/) <br>
- [ClawHub skill page](https://clawhub.ai/JarrodJS/seats-aero) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with API request parameters and summarized award availability results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a seats.aero API key supplied by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
