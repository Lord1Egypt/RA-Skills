## Description: <br>
Comprehensive interface for the SkedGo TripGo API, covering routing, public transport, trips, and location services. Use for multimodal journey planning, public transport data, and geocoding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanyu-zhang](https://clawhub.ai/user/guanyu-zhang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to call TripGo endpoints for multimodal routing, public transport data, trip management, location lookup, and geocoding. It is intended for applications that need scripted access to TripGo travel-planning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise travel searches, coordinates, event timing, trip IDs, webhook destinations, and analytics events are sent to TripGo as part of normal operation. <br>
Mitigation: Use the skill only when this data sharing is acceptable, avoid unnecessary home or work labels and exact locations, and use analytics or saved-trip endpoints only with appropriate consent and privacy coverage. <br>
Risk: Webhook registration can expose trip updates to callback destinations. <br>
Mitigation: Configure TRIPGO_WEBHOOK_ALLOWLIST before using hooks; keep TRIPGO_ALLOW_UNSAFE_WEBHOOK disabled except for trusted manual debugging. <br>
Risk: Deprecated TTP endpoints may be less suitable for new production workflows. <br>
Mitigation: Prefer non-deprecated routing and trip endpoints unless a reviewed use case specifically requires the TTP scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guanyu-zhang/skedgo-tripgo-api) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Routing Reference](references/routing.md) <br>
- [Trips Reference](references/trips.md) <br>
- [Geocode Reference](references/geocode.md) <br>
- [Locations Reference](references/locations.md) <br>
- [Public Transport Reference](references/public-transport.md) <br>
- [TTP Reference](references/ttp.md) <br>
- [TripGo Configuration Documentation](https://developer.tripgo.com/#/configuration) <br>
- [TripGo Geocoding Providers Documentation](https://developer.tripgo.com/extensions/#unlocking_geocoding_providers) <br>
- [TripGo Locations FAQ](https://developer.tripgo.com/faq/#locations-cell-ids-and-hash-codes) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with bash scripts and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRIPGO_API_KEY and the curl and jq binaries; API responses depend on TripGo service availability and requested endpoints.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
