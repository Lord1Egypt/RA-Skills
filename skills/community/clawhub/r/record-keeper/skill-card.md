## Description:

Record Keeper helps agents create, file, index, search, and manage structured work records using a closed set of record categories and Markdown templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckystarry](https://clawhub.ai/user/luckystarry)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team operators use this skill to turn meetings, requirements, plans, SOPs, reports, administrative notes, tasks, periodic summaries, memos, and quality cases into consistently named Markdown records. Developers and workspace maintainers can also use it to keep those records searchable and status-tracked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Record contents and search queries may be sent to an external embedding service.

Mitigation: Use only in workspaces where this data flow is approved, and redact or exclude confidential personnel, financial, customer, incident, credential, and unreleased planning data.

Risk: Broad local indexing can capture more workspace record data than intended.

Mitigation: Prefer explicit opt-in, category or file exclusions, local embeddings where available, and path validation before production use.

## Reference(s):

- [Record Keeper skill page](https://clawhub.ai/luckystarry/skills/record-keeper)
- [Meeting record template](references/meeting.md)
- [Requirement document template](references/requirement.md)
- [Plan template](references/plan.md)
- [SOP template](references/sop.md)
- [Report template](references/report.md)
- [Task template](references/task.md)
- [Weekly report template](references/weekly-report.md)
- [Monthly report template](references/monthly-report.md)
- [Quarterly report template](references/quarterly-report.md)
- [Yearly report template](references/yearly-report.md)
- [Vector index guide](references/vector-index.md)
- [Status transition rules](references/status-transitions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown records, concise guidance, and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates workspace record files under records/YYYY-MM and may update a local SQLite vector index and record status metadata.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
