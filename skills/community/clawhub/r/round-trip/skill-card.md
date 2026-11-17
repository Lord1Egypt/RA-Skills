## Description:

Helps agents search and present round-trip travel options through the flyai CLI, including outbound and return flight selection and related travel services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivan97](https://clawhub.ai/user/ivan97)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel agents use this skill to collect trip parameters, run real-time round-trip travel searches, and present bookable outbound and return options. The skill is intended for travel booking workflows that require CLI-backed results instead of model-generated travel data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a global npm package and execute shell commands.

Mitigation: Review the package source and run the skill in a contained environment before using it with real travel requests.

Risk: Travel itinerary details may be sent to a third-party flight service.

Mitigation: Use only when external travel data sharing is acceptable for the user and organization.

Risk: The skill may persist raw queries and command logs locally.

Mitigation: Confirm logging behavior and retention expectations before handling sensitive itinerary information.

Risk: Booking links and branding are added to the agent response.

Mitigation: Check that returned links come from CLI output and that users understand they are leaving the agent workflow to book.

## Reference(s):

- [Parameter and output templates](artifact/references/templates.md)
- [Round-trip search playbooks](artifact/references/playbooks.md)
- [Failure recovery fallbacks](artifact/references/fallbacks.md)
- [Execution log runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel results with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses flyai CLI output as the source for travel results; may include booking links, brand text, and local execution logging.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
