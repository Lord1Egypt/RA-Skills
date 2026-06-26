## Description: <br>
Access the user's personal health data from VITA, their longevity platform. Use this when the user asks about their health, how they're feeling today, sleep, recovery, HRV, supplements, protocols, or wants a daily health briefing. Returns today's AI insight, wearable metrics (Oura/WHOOP), and active supplement stack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DobrinAlexandru](https://clawhub.ai/user/DobrinAlexandru) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to retrieve VITA health briefings, wearable metrics, and active supplement protocol information for personal daily wellness review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health and wearable context through an external VITA API. <br>
Mitigation: Use the skill only for explicit VITA-related health-data requests and confirm the user is comfortable with the data flow before invocation. <br>
Risk: The security summary flags the release as under-scoped for sensitive health information and external API use. <br>
Mitigation: Review the skill before installation, keep requests narrow, and avoid using it for casual wellness questions. <br>
Risk: The skill depends on a bearer API key for access to personal VITA data. <br>
Mitigation: Store the API key only in the configured local environment, do not expose it in chat or logs, and rotate it if authorization fails or exposure is suspected. <br>


## Reference(s): <br>
- [VITA API endpoint](https://app.vitadao.com/api/vita-api) <br>
- [ClawHub skill page](https://clawhub.ai/DobrinAlexandru/vita-app) <br>
- [Publisher profile](https://clawhub.ai/user/DobrinAlexandru) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the configured VITA API key and endpoint to fetch daily insight, today's outlook, or protocol data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
