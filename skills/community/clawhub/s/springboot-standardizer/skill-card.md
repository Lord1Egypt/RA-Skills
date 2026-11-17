## Description:

A Chinese-language skill that helps developers analyze and standardize Spring Boot and MyBatis project structures, generate a standard layered project layout, and provide MyBatis, Redis, and Kafka configuration templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davieyang](https://clawhub.ai/user/davieyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Java Spring Boot and MyBatis projects for nonstandard structure, plan refactors into controller, service, DAO, entity, DTO, and VO layers, and generate starter project files and configuration templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write generated project files and analysis reports into user-selected directories, which may overwrite existing files.

Mitigation: Run it in a clean output directory or version-controlled workspace and review diffs before adopting generated files.

Risk: The generated Redis template uses Jackson default typing for Object values, a pattern the security evidence flags as dangerous for real applications.

Mitigation: Replace the Redis Object/default-typing template with a safer typed serializer approach before deploying generated code.

## Reference(s):

- [MyBatis Configuration Guide](references/mybatis-config.md)
- [Redis Configuration Template](references/redis-config.md)
- [Kafka Configuration Template](references/kafka-config.md)
- [Java SpringBoot Naming Conventions](references/naming-conventions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, and generated source or configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or overwrite files in the selected analysis or output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
