## Description:

A blind-box travel planning agent that uses a user's current city, departure date, trip length, and budget to recommend an unvisited destination and generate a relaxed itinerary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoxuanljj](https://clawhub.ai/user/haoxuanljj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent to create surprise leisure travel plans, including destination selection, budget allocation, relaxed daily activities, and booking-oriented itinerary summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store travel history and produce itineraries containing booking details, confirmation numbers, hotel addresses, and transport plans.

Mitigation: Keep generated itineraries private, avoid entering real confirmation numbers unless necessary, and review or delete local travel history when it is no longer needed.

Risk: Trip details may be sent to flyai or third-party booking services while searching for travel, lodging, attraction, weather, and transportation information.

Mitigation: Use the skill only when sharing those trip details with external services is acceptable, and review third-party links before booking.

Risk: Generated output may include local file paths for saved itinerary documents.

Mitigation: Verify output paths before writing files and store itinerary files only in locations appropriate for sensitive travel information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haoxuanljj/skills/travel-blind-box)
- [README](README.md)
- [Quickstart](QUICKSTART.md)
- [Examples](examples.md)
- [Testing guide](TESTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown itineraries, plain text summaries, JSON budget allocations, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party booking links, local output file paths, and locally stored travel history.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
