## Description:

Transform any AI agent into a world-class travel planner using Kontour AI's 9-dimension progressive planning model with structured conversation flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skylinehk](https://clawhub.ai/user/skylinehk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and travel operators use this skill to turn an agent into a structured travel-planning assistant that gathers trip requirements, compares destinations, drafts provisional itineraries, and prepares review-ready planning output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated booking-ready data or public planning links may expose itinerary, date, passenger, or budget details if shared prematurely.

Mitigation: Share generated links and booking-ready details only after user consent, and review operator-provided URLs before sending them to external services.

Risk: Offline reference data and route scaffolds may be stale or incomplete for live hours, transit, pricing, weather, availability, or booking constraints.

Mitigation: Treat plans as provisional until an operator validates live details and keeps visible caveats in traveler-facing output.

Risk: The artifact contains planned booking integrations but no active booking API connection.

Mitigation: Present integration entries as roadmap context only and do not claim live booking capability unless separately verified in the current release context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skylinehk/skills/travel-planner-notion-ai-obsidian-kontour-integration)
- [README](artifact/README.md)
- [Destinations reference data](artifact/references/destinations.json)
- [Airports reference data](artifact/references/airports.json)
- [Airlines reference data](artifact/references/airlines.json)
- [Activities reference data](artifact/references/activities.json)
- [Budget benchmarks](artifact/references/budget-benchmarks.json)
- [Booking integration roadmap](artifact/references/booking-integrations.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance, KML]

**Output Format:** [Markdown guidance with structured JSON, shell command examples, Google Maps URLs, and optional KML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline planning output from bundled reference data; generated recommendations should be live-validated before booking or final presentation.]

## Skill Version(s):

2.0.43 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
