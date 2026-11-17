## Description:

Calculate traffic-aware routes, travel times, and distances between locations using Google Routes API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vemec](https://clawhub.ai/user/vemec)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to calculate travel time, distance, and a navigation link between an origin and destination, with traffic-aware routing for driving trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Origin and destination addresses are sent to Google Routes API and printed in the JSON response.

Mitigation: Use the skill only when users are comfortable sharing those addresses with Google through their own API key, and avoid submitting sensitive addresses unless necessary.

Risk: BICYCLE and WALK requests can return a Google Maps link that still uses driving mode.

Mitigation: Verify the route mode in Google Maps before relying on non-driving directions.

Risk: Responses are requested with a fixed es-419 locale and metric units.

Mitigation: Check duration, distance, and route details against user expectations when locale-specific wording or units matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vemec/skills/smart-route)
- [Publisher profile](https://clawhub.ai/user/vemec)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON from a Node.js command, with setup guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the GOOGLE_ROUTES_API_KEY environment variable; route output includes origin, destination, mode, duration, distance, traffic duration seconds, and a Google Maps route link.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
