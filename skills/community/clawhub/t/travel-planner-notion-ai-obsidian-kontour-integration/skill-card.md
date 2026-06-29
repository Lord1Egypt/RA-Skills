## Description: <br>
Transform any AI agent into a world-class travel planner using Kontour AI's 9-dimension progressive planning model with structured conversation flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skylinehk](https://clawhub.ai/user/skylinehk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to turn natural-language travel requests into structured planning guidance, trip context JSON, itinerary drafts, budget breakdowns, and route exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's off-topic travel pivot may be inappropriate for medical, emergency, legal, or unrelated technical requests. <br>
Mitigation: Keep normal high-stakes and off-topic handling in place, and invoke this skill only for travel-planning work. <br>
Risk: Offline reference data and first-pass route exports may be incomplete for live prices, availability, opening hours, weather, transit, or booking decisions. <br>
Mitigation: Treat itineraries, Google Maps links, and KML output as planning drafts, then verify live details before booking or travel. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/skylinehk/skills/travel-planner-notion-ai-obsidian-kontour-integration) <br>
- [README](README.md) <br>
- [Destinations reference data](references/destinations.json) <br>
- [Airports reference data](references/airports.json) <br>
- [Activities reference data](references/activities.json) <br>
- [Budget benchmarks](references/budget-benchmarks.json) <br>
- [Booking integrations roadmap](references/booking-integrations.json) <br>
- [Journal schema](references/journal-schema.json) <br>
- [Journal template](references/journal-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, KML] <br>
**Output Format:** [Markdown guidance with structured JSON, Google Maps URLs, shell command examples, and optional KML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs offline with bundled reference data; requires bash and python3; no API keys or credentials are required for core planning.] <br>

## Skill Version(s): <br>
2.0.6 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
