## Description:

Plan cross-time-zone meeting windows for distributed teams, providing region-by-region local time mappings and tradeoff analysis for scheduling decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers can use this skill to compare cross-time-zone meeting windows, map local times by region, and explain scheduling tradeoffs before a meeting is booked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Representative aliases such as US, EU, and Asia can produce imprecise local-time mappings.

Mitigation: Ask users for exact IANA time zones or city-level locations when accuracy matters.

Risk: The skill does not validate live DST status, calendar availability, participant agreement, or sent invitations.

Mitigation: Manually confirm DST, availability, and meeting details before sending or relying on invitations.

Risk: Conflicting regional preferences may not have a perfect overlap.

Mitigation: State assumptions and hard constraints, then present the least-bad option with explicit tradeoffs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/time-zone-planner)
- [Time Zone Planner references](references/guidelines.md)
- [Audit Reference](references/audit-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with local-time tables, assumptions, tradeoffs, risk notes, and optional JSON-like scheduling output from the packaged script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided regions and meeting duration; exact IANA time zones or cities improve accuracy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
