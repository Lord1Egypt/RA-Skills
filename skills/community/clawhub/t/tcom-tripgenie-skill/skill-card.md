## Description:

TripGenie skill handles hotel booking, flight search, attraction recommendation, and travel consultation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthurchiao](https://clawhub.ai/user/arthurchiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to route travel requests to TripGenie for hotel booking, flight search, attraction recommendations, and trip planning. It is intended for travel queries where live Trip.com data, pricing, availability, or booking links are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel questions, itinerary details, locale information, and the TripGenie API token may be sent to Trip.com infrastructure.

Mitigation: Use the skill only for intended provider lookups, avoid sending unnecessary sensitive travel details, and configure the API key through a protected environment or secret manager.

Risk: Returned prices, availability, booking links, and related metadata are third-party content.

Mitigation: Verify booking details and links directly with the provider before acting on them.

Risk: Broad travel trigger patterns can route casual travel conversation to the external API.

Mitigation: Enable or invoke the skill only when a Trip.com lookup is intended.

## Reference(s):

- [TripGenie homepage](https://www.trip.com/tripgenie)
- [TripGenie OpenClaw token page](https://www.trip.com/tripgenie/openclaw)
- [ClawHub skill page](https://clawhub.ai/arthurchiao/skills/tcom-tripgenie-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/arthurchiao)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown API responses with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TRIPGENIE_API_KEY and may return third-party prices, availability, booking links, and related travel metadata.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
