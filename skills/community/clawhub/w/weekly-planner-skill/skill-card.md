## Description:

A weekly planning assistant that records plans, completions, and reflections, then generates daily work reports and weekly summaries from local weekly JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ludiansheng](https://clawhub.ai/user/ludiansheng)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users can use this skill to organize weekly plans, completion notes, and reflections. Agents use it to invoke the bundled planner script, persist weekly records, query progress, and draft daily or weekly reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command templates include user-controlled task text and could be unsafe if an agent runs shell-interpolated command strings.

Mitigation: Invoke the Python script with structured arguments, avoid shell interpolation, and review command previews before execution.

Risk: The skill persists planning data under ./weekly-plans.

Mitigation: Use it only where local persistence is expected and review stored records for sensitive personal or work information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ludiansheng/skills/weekly-planner-skill)
- [Data format](artifact/references/data-format.md)
- [Query templates](artifact/references/query-templates.md)
- [Daily report template](artifact/references/daily-report-template.md)
- [Weekly report template](artifact/references/weekly-report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists weekly planning records under ./weekly-plans.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
