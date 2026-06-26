## Description: <br>
Comprehensive interface for the TripGo API, covering routing, public transport, trips, and location services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanyu-zhang](https://clawhub.ai/user/guanyu-zhang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call TripGo endpoints for multimodal route planning, geocoding, public transport data, trip management, and location lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route searches, coordinates, schedules, trip identifiers, and related travel metadata are sent to TripGo. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid adding unnecessary sensitive labels such as home or work in requests. <br>
Risk: Webhook registration can expose trip update data to a callback endpoint. <br>
Mitigation: Keep HTTPS-only webhook validation and TRIPGO_WEBHOOK_ALLOWLIST enabled; use TRIPGO_ALLOW_UNSAFE_WEBHOOK only for trusted manual debugging. <br>
Risk: Some trip scripts save, update, mark, delete, or otherwise change remote trip state. <br>
Mitigation: Double-check trip and hook identifiers before running state-changing scripts. <br>
Risk: The artifact includes deprecated TripGo endpoints. <br>
Mitigation: Prefer non-deprecated routing and trip endpoints, and use deprecated scripts only when explicitly required and verified against live TripGo documentation. <br>


## Reference(s): <br>
- [TripGo API ClawHub Release](https://clawhub.ai/guanyu-zhang/tripgo-api) <br>
- [TripGo API](https://skedgo.com/tripgo-api/) <br>
- [TripGo Developer Documentation](https://developer.tripgo.com/) <br>
- [TripGo OpenAPI Spec](https://github.com/skedgo/tripgo-api) <br>
- [Configuration Section - TripGo API](references/configuration.md) <br>
- [Geocode API](references/geocode.md) <br>
- [Locations API](references/locations.md) <br>
- [Public Transport API](references/public-transport.md) <br>
- [TripGo API - Routing](references/routing.md) <br>
- [Trips API](references/trips.md) <br>
- [TTP (Travelling Tourist Problem)](references/ttp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and TRIPGO_API_KEY; some scripts modify remote trip state or register webhooks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
