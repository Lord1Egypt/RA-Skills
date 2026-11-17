## Description:

What Should We Do? helps an agent suggest personalized activities using weather, showtimes, streaming preferences, game libraries, group profiles, routines, favorites, business hours, ratings, calendar events, invitations, reminders, and RSVP tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottfo](https://clawhub.ai/user/scottfo)

### License/Terms of Use:


## Use Case:

External users use this skill to get activity, entertainment, dining, game night, date night, and group planning suggestions. It can personalize suggestions from stored preferences and history, then help schedule accepted plans, send invites, and track RSVP status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores activity preferences, routines, group membership, and contact details in the workspace.

Mitigation: Use it only where that local storage is acceptable, avoid storing third-party contact details without consent, and review stored preference and history files periodically.

Risk: Calendar, Places, Telegram, and cron actions may expose location, schedule, contact, or message details.

Mitigation: Confirm the exact data, recipients, message text, events, and reminders before allowing those actions.

Risk: Broad natural-language triggers can move from suggestion into scheduling, reminders, or outbound invites.

Mitigation: Require an explicit confirmation step before creating calendar events, adding cron jobs, sending invitations, or updating RSVP records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottfo/skills/whatdo)
- [Skill homepage](https://github.com/ScotTFO/whatdo-skill)
- [Google Calendar events endpoint](https://www.googleapis.com/calendar/v3/calendars/primary/events)
- [Google Places Text Search endpoint](https://places.googleapis.com/v1/places:searchText)
- [Google Places Nearby Search endpoint](https://places.googleapis.com/v1/places:searchNearby)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and conversational text with optional JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live-context checks, saved preference updates, calendar or reminder commands, invite messages, and RSVP summaries.]

## Skill Version(s):

2.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
