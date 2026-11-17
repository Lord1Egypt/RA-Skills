## Description:

This skill helps an agent query data, explore available data tools, and execute data operations through the SmartChart CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnyan2017](https://clawhub.ai/user/johnyan2017)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data-focused users use this skill to discover SmartChart datasets, inspect tool parameters, run SmartChart CLI queries, and format retrieved results for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a local SmartChart CLI and Python package, so an incorrect or untrusted installation could affect query behavior.

Mitigation: Install SmartChart in a dedicated virtual environment when possible and verify the package source before installing or upgrading.

Risk: The skill runs SmartChart data queries through the user's CLI environment.

Mitigation: Use the skill only when the user intends to query data through SmartChart, and review tool names and parameters before execution.

## Reference(s):

- [SmartChart skill page](https://clawhub.ai/johnyan2017/skills/smartchart)
- [SmartChart tool parameter reference](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and formatted query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-formatted SmartChart CLI output when the selected tool supports JSON format.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
