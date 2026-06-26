## Description: <br>
TripGenie skill handles hotel booking, flight search, attraction recommendation, and travel consultation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArthurChiao](https://clawhub.ai/user/ArthurChiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to route hotel, flight, attraction, and general travel requests to TripGenie for current travel results and booking-oriented responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel prompts and booking searches are sent to a third-party Trip.com API. <br>
Mitigation: Avoid entering highly sensitive personal details unless the deployment has approved this data sharing. <br>
Risk: The skill depends on TRIPGENIE_API_KEY for API access. <br>
Mitigation: Store the key securely, limit exposure in logs or prompts, and rotate it if it is disclosed. <br>
Risk: Returned booking links and provider text are third-party content. <br>
Mitigation: Review prices, terms, availability, and provider details before acting on booking results. <br>


## Reference(s): <br>
- [Trip.com TripGenie](https://www.trip.com/tripgenie) <br>
- [TripGenie OpenClaw Setup](https://www.trip.com/tripgenie/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/ArthurChiao/tcom-tripgenie-skill) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline bash examples for API calls and setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRIPGENIE_API_KEY and sends user travel queries to TripGenie API endpoints.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
