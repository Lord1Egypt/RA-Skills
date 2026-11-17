## Description:

Add trip itineraries, flights, hotel check-ins, and activities to Google Calendar using gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swayamg20](https://clawhub.ai/user/swayamg20)

### License/Terms of Use:


## Use Case:

External users use this skill to turn confirmed travel plans, boarding pass details, hotel stays, and major activities into Google Calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted itinerary or boarding pass text could be incorporated into calendar creation commands.

Mitigation: Review event titles, locations, descriptions, dates, and time zones before approving calendar creation; prefer direct argument execution or explicit escaping for parsed text.

Risk: The skill requires gog access that can create Google Calendar events.

Mitigation: Install only when that calendar access is acceptable, and keep explicit user confirmation before creating any events.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline gog CLI commands and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gog CLI access to create Google Calendar events.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
