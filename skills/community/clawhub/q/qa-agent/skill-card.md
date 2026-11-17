## Description:

Un agente para realizar tareas de control de calidad (QA), incluyendo analisis de codigo, ejecucion de pruebas y reporte de problemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steven-mr3](https://clawhub.ai/user/steven-mr3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to run local Python and JavaScript linting and tests, then summarize defects, warnings, and test outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running test frameworks can execute code from the target project.

Mitigation: Run tests only against projects and paths you trust, preferably in an isolated workspace when reviewing unfamiliar code.

Risk: Fixer flags such as ruff --fix or eslint --fix can modify project files.

Mitigation: Review the target path and use version control or backups before enabling automatic fixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steven-mr3/skills/qa-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell commands and QA result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include lint findings, test results, file paths, line references, and suggested fixes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
