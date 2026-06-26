## Description: <br>
Read upcoming TripIt travel plans from a TripIt iCal feed; use for next trip, upcoming travel, itinerary, flight or hotel bookings already in TripIt; do not use for live flight status, delays, check-in, or general travel research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caddytan](https://clawhub.ai/user/caddytan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to retrieve and summarize upcoming itinerary items already saved in TripIt. It is intended for TripIt calendar lookups, not live travel operations or new travel research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The TripIt iCal feed can expose private future travel details, including lodging, transportation, locations, and itinerary timing. <br>
Mitigation: Keep TRIPIT_ICAL_URL secret, rotate the feed URL if exposed, and review summaries before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caddytan/tripit-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the script, summarized by the agent as concise Markdown or text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python with requests and icalendar plus a TRIPIT_ICAL_URL environment value or command argument; upcoming_events is limited to 20 items.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
