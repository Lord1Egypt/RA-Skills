## Description:

Helps migrate Java Spring Boot projects from Swagger 2 (Springfox) to OpenAPI 3.0 (SpringDoc), including annotation replacements, import updates, and Javax-to-Jakarta package migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangteng85859](https://clawhub.ai/user/wangteng85859)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan or automate migration of Spring Boot API documentation from Springfox Swagger 2 to SpringDoc OpenAPI 3, then review complex annotations and dependency changes before committing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration scripts can follow symlinked Java files and modify files outside the selected project.

Mitigation: Run only on trusted projects, check for symlinked .java files, use --dry-run first, keep the project under version control, and review the diff before committing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangteng85859/skills/swagger2-to-openapi3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Java examples and optional shell/Python migration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run previews; generated code changes require human review before commit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
