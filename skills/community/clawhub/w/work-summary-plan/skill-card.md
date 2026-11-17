## Description:

Extracts Youdao Note work logs, classifies work items, and generates work distribution analysis and time allocation planning reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ydyzzjsl](https://clawhub.ai/user/ydyzzjsl)

### License/Terms of Use:

MIT-0

## Use Case:

Managers and professionals who keep work logs in Youdao Note use this skill to review actual note content, understand work distribution, and plan future time allocation. It is especially aimed at technical managers, project managers, and similar roles that need structured review and time management from work logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a Youdao Note personal Key and accesses work notes that may contain sensitive business information.

Mitigation: Treat the Key like a password, limit the note search scope, and review extracted note content before sharing reports.

Risk: Generated reports and retained memory may contain sensitive findings derived from work notes.

Mitigation: Store generated reports and .workbuddy/memory/ only in approved locations, remove unneeded retained data, and avoid including confidential details in shared outputs.

Risk: HTML reports use active chart scripts and note-derived fields.

Mitigation: Prefer an updated version that sanitizes note-derived report fields and bundles or verifies Chart.js before opening or distributing generated HTML.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ydyzzjsl/skills/work-summary-plan)
- [Report generation specification](artifact/references/report_spec.md)
- [Work category system](artifact/references/work_categories.md)
- [Chart.js 4.4.0 CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces work analysis and time allocation planning reports from extracted note content; may retain derived findings in .workbuddy/memory/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
