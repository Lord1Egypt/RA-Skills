## Description:

Converts MySQL CREATE TABLE statements into Java entity classes with MyBatis-Plus or JPA annotations, type mapping, and snake_case-to-camelCase naming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coder-myj](https://clawhub.ai/user/coder-myj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert MySQL DDL into Java entity classes for ORM models, including package, base-class, annotation-style, type-mapping, and getter/setter decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated entity classes may use an annotation style, nullable field type, or primary-key strategy that does not match the target project.

Mitigation: Review generated classes before use, especially annotation style, nullable field types, and primary-key strategy.

Risk: Database schema comments may expose sensitive business details if copied into generated source code.

Mitigation: Review, redact, or omit schema-derived comments before committing generated entity classes.

## Reference(s):

- [MySQL to Java Type Mappings](references/type_mappings.md)
- [ClawHub skill page](https://clawhub.ai/coder-myj/skills/sql-to-java)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown containing Java code blocks and concise generation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates Java entity classes from provided MySQL CREATE TABLE statements; framework annotations depend on user or project context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
