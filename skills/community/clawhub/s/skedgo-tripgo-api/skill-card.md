## Description:

Comprehensive interface for the SkedGo TripGo API, covering routing, public transport, trips, and location services. Use for multimodal journey planning, public transport data, and geocoding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanyu-zhang](https://clawhub.ai/user/guanyu-zhang)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to plan multimodal trips, look up public transport services, manage TripGo trips, retrieve location data, and perform geocoding through TripGo API scripts and references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TripGo API requests can expose API keys and sensitive travel, trip, location, or webhook data to the configured API service.

Mitigation: Keep TRIPGO_API_KEY private, use the default official HTTPS TripGo API endpoint, and avoid setting TRIPGO_BASE_URL to untrusted hosts.

Risk: Webhook registration can send callbacks to external destinations.

Mitigation: Use TRIPGO_WEBHOOK_ALLOWLIST for approved webhook domains and reserve TRIPGO_ALLOW_UNSAFE_WEBHOOK=true for controlled debugging only.

Risk: Deprecated endpoints may have reduced support or changing behavior.

Mitigation: Avoid deprecated TTP and skedgoify scripts for production workflows unless their behavior is verified against the live TripGo API.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guanyu-zhang/skills/skedgo-tripgo-api)
- [TripGo developer documentation](https://developer.tripgo.com/)
- [TripGo API base endpoint](https://api.tripgo.com/v1)
- [Configuration reference](references/configuration.md)
- [Routing reference](references/routing.md)
- [Trips reference](references/trips.md)
- [Geocode reference](references/geocode.md)
- [Locations reference](references/locations.md)
- [Public transport reference](references/public-transport.md)
- [Travelling Tourist Problem reference](references/ttp.md)
- [TripGo geocoding providers](https://developer.tripgo.com/extensions/#unlocking_geocoding_providers)
- [TripGo locations FAQ](https://developer.tripgo.com/faq/#locations-cell-ids-and-hash-codes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash scripts and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and TRIPGO_API_KEY; some scripts optionally use python3 for JSON formatting.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
