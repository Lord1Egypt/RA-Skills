## Description:

Matches a pet's face to its vaccination record and reports whether a configured vaccination reminder is due; it does not provide medical advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet hospital, boarding center, and pet insurance staff can use the skill to match a submitted pet image or video to a vaccination record and identify reminders that are due or overdue. It also supports queries for past reminder reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious because its reported account, user-management, and data-handling capabilities extend beyond its described reminders, and scan coverage is incomplete.

Mitigation: Before installing, clarify the extra account, identity, database, and data-transfer behavior, and verify that the export-only option avoids analysis.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-vaccination-reminder-analysis)

## Skill Output:

**Output Type(s):** [Analysis report, JSON, Markdown]

**Output Format:** [Structured vaccination reminder results with report links; Markdown report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports compare a linked vaccination record with the configured reminder cycle; the skill states that it does not provide medical advice.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
