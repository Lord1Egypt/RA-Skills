## Description:

Search award flight availability via seats.aero API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarrodjs](https://clawhub.ai/user/jarrodjs)

### License/Terms of Use:


## Use Case:

External users and travel-focused agents use this skill to search award flight availability, mileage booking options, premium-cabin redemptions, monitored routes, and trip details through the seats.aero partner API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user for a seats.aero API key, which is sensitive account access material.

Mitigation: Enter the key only when needed, avoid sharing broad-privilege keys, and rotate the key if it may have appeared in logs or transcripts.

Risk: Award availability data can become stale after it is retrieved.

Mitigation: Check the returned data freshness field and verify availability with the booking program before making travel decisions.

## Reference(s):

- [Seats.aero Partner API](https://seats.aero/partnerapi/)
- [Seats.aero Partner API Key](https://seats.aero/partner)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Configuration]

**Output Format:** [Markdown with API parameters, request guidance, and summarized flight availability details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a user-provided seats.aero API key and may include route, cabin, date, mileage cost, availability, data freshness, and booking-detail fields.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
