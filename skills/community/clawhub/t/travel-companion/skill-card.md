## Description:

Travel Companion helps agents create persistent, shareable travel plans with real place data, interactive maps, optimized routes, hotel and sightseeing recommendations, packing checklists, and collaborative editing through Aizzie.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hehachris](https://clawhub.ai/user/hehachris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel planners use this skill to turn travel requests into multi-day itineraries with real places, mapped routes, hotels, restaurants, sightseeing stops, packing lists, and shareable saved plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel plans, dates, places, and companion details may be sent to and persisted on aizzie.ai.

Mitigation: Get user consent before saving or sharing trips, and avoid entering sensitive personal details unless necessary.

Risk: The skill runs a mutable npm CLI at runtime using @latest.

Mitigation: Prefer a pinned, reviewed Aizzie CLI version when installing or operating the skill.

Risk: Persistent and shareable itineraries can expose trip information to unintended viewers if links are shared broadly.

Mitigation: Share trip links only with intended collaborators and review itinerary contents before distribution.

## Reference(s):

- [Aizzie homepage](https://aizzie.ai)
- [Travel Companion on ClawHub](https://clawhub.ai/hehachris/skills/travel-companion)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel-planning guidance with inline Aizzie CLI commands and saved-plan status notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent itineraries, maps, routes, checklists, and shareable collaboration links through aizzie.ai.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
