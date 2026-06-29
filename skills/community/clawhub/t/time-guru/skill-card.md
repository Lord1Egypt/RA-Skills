## Description: <br>
Natural language time tracking with smart activity classification, multi-dimensional reports, productivity analytics, and billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, freelancers, and knowledge workers use this skill to log work time in natural language, run timers, review productivity trends, and calculate billable time for projects or clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores detailed work logs, notes, project names, and billing data on local disk. <br>
Mitigation: Install only when local storage is acceptable, and avoid entering confidential client details unless they can be stored under ~/.openclaw/data/time-guru. <br>
Risk: Exports may contain sensitive time, project, and billing history. <br>
Mitigation: Treat exported CSV, JSON, and Markdown files as sensitive records and choose export destinations carefully. <br>


## Reference(s): <br>
- [Time Guru release page](https://clawhub.ai/harrylabsj/time-guru) <br>
- [Reference index](references/README.md) <br>
- [Activity categories](references/categories.json) <br>
- [Example queries](references/example-queries.md) <br>
- [Input schema](schemas/input.schema.json) <br>
- [Output schema](schemas/output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, csv, guidance] <br>
**Output Format:** [Text, Markdown, JSON, or CSV depending on the requested action and output format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local time logs, backups, billing configuration, and exports under ~/.openclaw/data/time-guru.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
