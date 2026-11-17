## Description:

Fetch real-time SL (Stockholm public transport) departures and deviation information using a Python CLI tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query Stockholm public transport departures, route options, and service deviations, and to maintain favorites for recurring checks.

### Deployment Geography for Use:

Global; operational data covers Stockholm, Sweden.

## Known Risks and Mitigations:

Risk: The preferences override can read from or overwrite arbitrary local paths instead of staying within the documented workspace preferences file.

Mitigation: Use the documented .sl/preferences.json storage path and avoid invoking commands with --preferences pointing elsewhere.

Risk: Saved favorite stops and routes may reveal location or routine data.

Mitigation: Treat saved favorites as sensitive local data and remove them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patello/skills/sl-trafiklab-api)
- [SL Trafiklab CLI and API References](references/api.md)
- [SL Transport API Reference](references/sl_transport_spec.md)
- [SL Deviations API Reference](references/sl_deviations_spec.md)
- [SL Journey Planner v2 Trips API Reference](references/journey_planner_v2_spec.md)
- [SL Transport API](https://transport.integration.sl.se/v1)
- [SL Deviations API](https://deviations.integration.sl.se/v1)
- [SL Journey Planner API](https://journeyplanner.integration.sl.se/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and JSON preference snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke live SL API requests and read or write saved favorites in .sl/preferences.json.]

## Skill Version(s):

3.7.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
