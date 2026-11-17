## Description:

Read upcoming TripIt travel plans from a TripIt iCal feed; use for next trip, upcoming travel, itinerary, flight or hotel bookings already in TripIt; do not use for live flight status, delays, check-in, or general travel research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caddytan](https://clawhub.ai/user/caddytan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about upcoming trips, flights, hotels, trains, or car bookings that are already present in the user's TripIt itinerary feed. It should not be used for live flight status, travel research, weather, visa guidance, or details absent from the returned itinerary data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A private TripIt iCal URL can expose itinerary details or feed-token data if logged, shared, or passed through an uncontrolled environment.

Mitigation: Use an HTTPS TripIt feed URL only, keep TRIPIT_ICAL_URL in a controlled environment, and redact feed URLs from errors or shared outputs.

Risk: The script can read .env values from the current directory, so unrelated local environment files could change which feed is fetched.

Mitigation: Run the skill from a controlled workspace and set TRIPIT_ICAL_URL explicitly for the agent process.

Risk: Dependencies are listed without pinned versions.

Mitigation: Pin and review the requests and icalendar dependency versions before routine or organizational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caddytan/skills/tripit-calendar)
- [Publisher profile](https://clawhub.ai/user/caddytan)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON from the script, with concise natural-language summaries for the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRIPIT_ICAL_URL plus Python dependencies requests and icalendar; the script returns up to 20 upcoming events.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
