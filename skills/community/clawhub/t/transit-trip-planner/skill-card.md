## Description:

AirnodeHub transit skill to plan transit, walking, and driving trips; compare routes, check live departures or disruptions, geocode places, and verify Airnode attestations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metobom](https://clawhub.ai/user/metobom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan transit, walking, or driving trips, compare route options, check live departures or disruptions, and present actionable route details with provenance and verification status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise locations, travel times, route constraints, and accessibility needs may be sent to BusMaps or Geoapify to compute routes.

Mitigation: Use the least precise request that still satisfies the trip-planning need, disclose the data-sharing scope, and avoid unnecessary expansion of route-service calls.

Risk: Potentially paid route-service operations may create unexpected cost if expanded silently.

Mitigation: State the bounded scope and known or uncertain cost before any potentially paid POST operation, and proceed only after explicit approval.

Risk: Attestation or real-time status may be overstated when signatures, freshness, or live fields are unavailable.

Mitigation: Report verification status, freshness, and missing live fields plainly; state when an attestation was not cryptographically verified.

## Reference(s):

- [Airnode BusMaps Documentation](https://airnode-busmaps.fly.dev/)
- [Airnode Geoapify Documentation](https://airnode-geoapify.fly.dev/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown route guidance with route details, costs, attributions, provenance, and verification status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bounded external route-service requests when required and approved.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
