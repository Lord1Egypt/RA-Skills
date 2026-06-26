## Description: <br>
Add trip itineraries, flights, hotel check-ins, and activities to Google Calendar using gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swayamg20](https://clawhub.ai/user/swayamg20) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Travelers and assistants use this skill to convert finalized trip plans, boarding passes, hotel stays, and major activities into Google Calendar events after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar events may contain incorrect dates, times, timezones, locations, or descriptions if itinerary details are ambiguous or untrusted. <br>
Mitigation: Review every event title, date, time, timezone, location, and description before confirming creation. <br>
Risk: The skill creates events through the local gog CLI, which uses the configured Google account. <br>
Mitigation: Install only when gog is already trusted for the intended Google account and decline event creation if the account or calendar target is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swayamg20/trip-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and confirmation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog CLI and user review before creating calendar events.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
