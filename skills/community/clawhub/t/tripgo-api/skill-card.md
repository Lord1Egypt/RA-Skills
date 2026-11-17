## Description:

Comprehensive interface for the TripGo API, covering routing, public transport, trips, and location services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanyu-zhang](https://clawhub.ai/user/guanyu-zhang)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to call TripGo endpoints for multimodal journey planning, public transport data, trip management, geocoding, and location lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests can use a custom TRIPGO_BASE_URL, which may send API keys and travel data to an unintended host.

Mitigation: Keep TRIPGO_BASE_URL unset unless intentionally using a trusted TripGo-compatible endpoint, and avoid passing API keys on the command line.

Risk: Trip coordinates, trip IDs, webhook callback URLs, and analytics calls can reveal sensitive travel activity.

Mitigation: Treat these values as sensitive data, restrict where they are logged or shared, and run the scripts only in controlled environments.

Risk: Webhook registration can expose trip update data to callback endpoints.

Mitigation: Use HTTPS callback URLs and configure TRIPGO_WEBHOOK_ALLOWLIST; do not set TRIPGO_ALLOW_UNSAFE_WEBHOOK except for trusted manual debugging.

Risk: Deprecated endpoints are included for backward compatibility.

Mitigation: Prefer current endpoints for new workflows and avoid deprecated TTP or routing scripts unless compatibility requires them.

## Reference(s):

- [TripGo API skill page](https://clawhub.ai/guanyu-zhang/skills/tripgo-api)
- [TripGo API access](https://skedgo.com/tripgo-api/)
- [TripGo developer documentation](https://developer.tripgo.com/)
- [Configuration reference](references/configuration.md)
- [Routing reference](references/routing.md)
- [Trips reference](references/trips.md)
- [Public transport reference](references/public-transport.md)
- [Geocode reference](references/geocode.md)
- [Locations reference](references/locations.md)
- [TTP reference](references/ttp.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and TRIPGO_API_KEY; some scripts optionally use TRIPGO_BASE_URL and webhook allowlist settings.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-03-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
