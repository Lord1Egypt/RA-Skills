## Description:

Generates Waze navigation links for addresses, establishments, and calendar-event locations, resolving vague destinations against the user's city before producing a clickable route link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dicasdomaroto-maker](https://clawhub.ai/user/dicasdomaroto-maker)

### License/Terms of Use:


## Use Case:

Users and assistants use this skill to create clean, clickable Waze route links for explicit destinations or scheduled events with locations. It is also intended to resolve vague local destination requests, such as nearby businesses, using the user's city.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read broad profile files and use city, state, destination, or calendar-location details when resolving routes.

Mitigation: Limit use to explicit user requests or approved profile fields, and confirm before sending sensitive location or agenda context to external search services.

Risk: Automatic briefing integration can create navigation links from calendar locations without a separate user request.

Mitigation: Review calendar-location handling before deployment and require confirmation for sensitive events or workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dicasdomaroto-maker/skills/waze)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown links with destination text and Waze deep links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include URL-encoded destination strings for Waze navigation.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
