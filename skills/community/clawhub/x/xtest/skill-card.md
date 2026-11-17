## Description:

xtest is a QA gatekeeping skill that has an agent classify code, script, or configuration changes, generate and run suitable validation, attempt up to three minimal repair cycles, and pass or reject delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqdwinding](https://clawhub.ai/user/zqdwinding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use xtest before delivering code, script, or configuration changes to choose an appropriate validation level, run tests or validation commands, and report pass or reject outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to run validation commands before delivery.

Mitigation: Review generated commands and run them in an appropriate development or CI environment before accepting results.

Risk: The skill may cause an agent to make repair edits when validation fails.

Mitigation: Keep repair edits limited to the current change, review diffs, and rerun validation before delivery.

Risk: Broad Chinese trigger phrases may activate the gatekeeping workflow in many code-delivery contexts.

Mitigation: Use the skill where mandatory pre-delivery validation is desired and confirm scope before execution.

## Reference(s):

- [ClawHub skill page: xtest](https://clawhub.ai/zqdwinding/skills/xtest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown validation plans and reports with inline shell commands and proposed code or configuration edits when repairs are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation is scoped to the current change and may include up to three repair-and-retest cycles before pass or reject.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
