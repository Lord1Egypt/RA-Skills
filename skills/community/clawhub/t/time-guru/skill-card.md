## Description:

Natural language time tracking with smart activity classification, multi-dimensional reports, productivity analytics, and billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to log activities in natural language, run timers, review daily or weekly productivity, track goals, and calculate billable project time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Time entries may contain client names, billing details, confidential project names, or sensitive notes persisted under ~/.openclaw/data/time-guru.

Mitigation: Review data sensitivity before use, restrict local file access, and avoid logging confidential details unless local persistence is acceptable.

Risk: Individual activity descriptions may be sent to a third-party parsing model.

Mitigation: Avoid entering sensitive descriptions unless third-party parsing of those descriptions is acceptable.

Risk: CSV exports and unrestricted export paths need review before use with untrusted imported data.

Mitigation: Review exported files before opening them in spreadsheet tools, avoid untrusted imports, and restrict export destinations until CSV formula sanitization and export path controls are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/time-guru)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)
- [Reference README](references/README.md)
- [Activity categories](references/categories.json)
- [Example Time-Guru Queries](references/example-queries.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Guidance]

**Output Format:** [Human-readable reports and structured JSON/CSV/Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include logged activities, time totals, category and project summaries, productivity recommendations, goal status, and billing amounts.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill manifest, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
