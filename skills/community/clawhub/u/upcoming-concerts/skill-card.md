## Description: <br>
Search for upcoming concerts and live music events by city, country, artist, or genre using the Ticketmaster Discovery API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PatFitzner](https://clawhub.ai/user/PatFitzner) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find upcoming concerts and live music events for a city, country, artist, genre, or date range using Ticketmaster event data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticketmaster API key exposure through shared terminals, logs, or copied error output. <br>
Mitigation: Use a dedicated Ticketmaster developer key and avoid sharing logs or command output that may include API details. <br>
Risk: Network requests are sent to Ticketmaster for event searches. <br>
Mitigation: Run the skill only when Ticketmaster API use is acceptable for the user's query and environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PatFitzner/upcoming-concerts) <br>
- [Ticketmaster Developer Portal](https://developer.ticketmaster.com/) <br>
- [Ticketmaster Discovery API events endpoint](https://app.ticketmaster.com/discovery/v2/events.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON array from the helper script, normally summarized for the user as a readable Markdown table sorted by date.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a TICKETMASTER_API_KEY environment variable; accepts optional city, country, artist, genre, date range, and result size filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
