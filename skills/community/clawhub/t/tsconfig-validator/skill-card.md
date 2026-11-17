## Description:

Validate and lint tsconfig.json files for common mistakes, conflicting compiler options, strictness gaps, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to lint, validate, audit, and check TypeScript configuration files for structural issues, strictness gaps, compatibility problems, and best-practice findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script against a tsconfig path provided by the user.

Mitigation: Review agent prompts before execution and keep use scoped to TypeScript configuration validation.

Risk: Lint findings may be advisory and could be inappropriate for a project's intended TypeScript setup.

Mitigation: Review reported warnings and informational findings against project requirements before changing configuration.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown issue reports with rule names, severities, line numbers, messages, and summary counts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against a user-provided tsconfig path and reports findings without requiring credentials or network access.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
