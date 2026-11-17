## Description:

Solo Trip helps agents plan solo travel with real-time flight, lodging, attraction, itinerary, and booking-link results powered by the flyai CLI and Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to plan solo trips, compare flights, hotels, attractions, and itineraries, and receive user-facing Markdown results with booking links. The skill is intended for solo city, adventure, and safety-focused trip planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and trusting a global third-party travel CLI.

Mitigation: Review the CLI package, pin or approve the installed version where possible, and run it only in environments where third-party CLI execution is allowed.

Risk: Trip details may be sent to the external travel service and raw request logs may be retained locally.

Mitigation: Avoid entering sensitive travel data unless the user accepts that disclosure path, and configure log retention or deletion for local execution logs.

Risk: The booking-link requirement can steer outputs toward a single travel provider's available inventory.

Mitigation: Tell users when results are limited to the flyai/Fliggy data source and encourage independent review before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/solo-trip)
- [Output templates](references/templates.md)
- [Scenario playbooks](references/playbooks.md)
- [Fallback procedures](references/fallbacks.md)
- [Execution log runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links, comparison tables, and occasional inline shell commands for retry or setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires successful flyai CLI output for travel data; booking results are expected to include detailUrl-backed Book links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
