## Description:

Compiles complex business goals into statically validated workflow execution plans (Plan IR).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to break complex business goals into DAG-based workflow plans, bind steps to approved skills, and produce validation reports before a downstream workflow engine executes anything.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation results are structural checks and should not be treated as a complete authorization boundary.

Mitigation: Enforce permissions, tenant boundaries, condition-expression parsing, and human review separately before executing high-impact workflow actions.

Risk: A valid plan can still encode incorrect, overbroad, or risky business steps.

Mitigation: Review generated plans before execution, especially for financial, personnel, or other high-impact workflows.

## Reference(s):

- [Orchestration Rules](references/orchestration_rules.md)
- [DAG Patterns](references/dag_patterns.md)
- [Scope Rules](references/scope_rules.md)
- [Security Guardrails](references/security_guardrails.md)
- [Plan IR Output Schema](assets/output_schema.json)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON Plan IR and validation report, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plans and validation reports only; business action execution is delegated to a separate workflow engine.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
