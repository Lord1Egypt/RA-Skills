## Description:

Track urgent appointment calls across multiple providers with a live availability board, call log, openings, callbacks, and confirmation details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to organize urgent scheduling calls, compare openings by logistics, track callbacks and waitlists, and confirm appointment details before relying on a slot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some examples encourage portal monitoring and one-tap booking beyond a logistics-only document workflow.

Mitigation: Remove portal-monitoring and booking-link behavior; keep the skill limited to user-provided availability, call tracking, and confirmation reminders.

Risk: Some examples encourage assembling sensitive medical or insurance materials.

Mitigation: Do not request, store, summarize, or package insurance-card images, medical reports, verification codes, passwords, or other sensitive records in this skill.

Risk: Some examples refer users to unofficial scalper booking channels.

Mitigation: Direct users to official appointment channels and licensed professional routes, with emergency escalation when immediate harm or severe symptoms are described.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/urgent-appointment-scramble-board)
- [README](artifact/README.md)
- [Acceptance Tests](artifact/ACCEPTANCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown live board with tables, a call script, ranked options, a call log, and a confirmation checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document-only prompt-flow output; no executable code, API calls, network access, or credentials required.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact metadata also contains 1.0.1 and SKILL.md frontmatter contains 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
