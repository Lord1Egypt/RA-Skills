## Description: <br>
Fetches real-time SL (Stockholm public transport) departures and deviation information for stop, route, delay, and autonomous monitoring queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patello](https://clawhub.ai/user/patello) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check upcoming Stockholm public transport departures, inspect active disruptions, and maintain local favourite stops or routes for background monitoring. <br>

### Deployment Geography for Use: <br>
Global; transit data and route planning are scoped to Stockholm, Sweden. <br>

## Known Risks and Mitigations: <br>
Risk: Saved favourite stops and routes can reveal commuting habits. <br>
Mitigation: Store .sl/preferences.json locally with appropriate workspace access controls and enable autonomous monitoring only for routes the user intentionally wants watched. <br>
Risk: Autonomous disruption monitoring can produce irrelevant notifications if route-specific disruptions are not filtered. <br>
Mitigation: Apply the documented route-leg filtering logic and notify only when a new deviation affects the saved boarding, alighting, transfer stop, or whole line. <br>


## Reference(s): <br>
- [SL Trafiklab API References](references/api.md) <br>
- [SL Transport Integration API](https://transport.integration.sl.se/v1) <br>
- [ClawHub Release Page](https://clawhub.ai/patello/sl-trafiklab-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl and jq commands plus JSON preference snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; may write local autonomous monitoring preferences to .sl/preferences.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
