## Description:

Generate complete, image-rich travel plans from trip dates and destination, including day-by-day itinerary, transportation, lodging area guidance, budget ranges, local transit notes, and risk/backup plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daiwk](https://clawhub.ai/user/daiwk)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to turn a destination and exact trip dates into a structured, image-ready travel itinerary with routing, lodging-area guidance, budgets, booking checkpoints, and contingency planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can overwrite existing Markdown files when an output path points to an existing file.

Mitigation: Use a dedicated output folder and avoid allowing writes over existing Markdown unless replacement is explicitly intended.

Risk: User- or third-party-controlled Markdown fields such as image URLs or currency values can produce misleading itinerary content.

Mitigation: Use trusted HTTPS image URLs, avoid untrusted formatting inputs, and review generated Markdown before sharing.

Risk: Travel details such as weather, schedules, entry policy, and opening hours can be stale or incorrect if not checked during the current run.

Mitigation: Verify time-sensitive travel facts with primary sources and keep uncertain details labeled until confirmed.

## Reference(s):

- [Travel Research Checklist](references/research-checklist.md)
- [Output Specification](references/output-spec.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown itinerary draft with optional inline image URLs and command-line generation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated itinerary includes placeholders and a verification log for time-sensitive travel facts that must be checked before final delivery.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
