## Description:

Search for upcoming concerts and live music events by city, country, artist, or genre using the Ticketmaster Discovery API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patfitzner](https://clawhub.ai/user/patfitzner)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find upcoming live music events by location, artist, genre, and date range, then present Ticketmaster results as a readable date-sorted table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Ticketmaster API key and sends user-requested search parameters to Ticketmaster.

Mitigation: Use a scoped Ticketmaster key where possible, avoid submitting sensitive search terms, and rotate the key if exposure is suspected.

Risk: Concert results depend on Ticketmaster API availability and response quality.

Mitigation: Treat returned listings as current API results and verify important event details on the linked Ticketmaster event page before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patfitzner/skills/upcoming-concerts)
- [Ticketmaster Developer Portal](https://developer.ticketmaster.com/)
- [Ticketmaster Discovery API events endpoint](https://app.ticketmaster.com/discovery/v2/events.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-derived event tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TICKETMASTER_API_KEY and returns date-sorted concert results including event date, name, artists, venue, city, country, genre, and URL.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
