## Description:

Quality-driven development with automatic TDD/DDD methodology selection and TRUST 5 quality framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimky1122](https://clawhub.ai/user/kimky1122)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to structure coding work around project analysis, SPEC documentation, TDD or DDD execution, logging, tests, and a TRUST 5 quality gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses broad coding-task activation and can cause an agent to apply a strict quality workflow where a lighter workflow may be expected.

Mitigation: Confirm that the task should follow the QDD workflow before applying its SPEC, testing, logging, and quality-gate requirements.

Risk: The skill requires logs on changed code paths, which could expose sensitive data if log content is chosen poorly.

Mitigation: Review log messages before completion and exclude passwords, tokens, personal information, and other sensitive values.

## Reference(s):

- [TDD Patterns Reference](references/tdd-patterns.md)
- [DDD Patterns Reference](references/ddd-patterns.md)
- [TRUST 5 Quality Checklist](references/trust5-checklist.md)
- [ClawHub skill page](https://clawhub.ai/kimky1122/skills/quality-driven-dev)
- [Publisher profile](https://clawhub.ai/user/kimky1122)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, command, configuration, SPEC, progress-report, and completion-report snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can prompt the agent to create files, edit code, run tests or coverage commands, and report logging and TRUST 5 quality-gate results.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
