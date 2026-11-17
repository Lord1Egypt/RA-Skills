## Description:

Provides Spring Boot, MyBatis, and MySQL testing guidance for normal-flow, exception, boundary, mapper, service, controller, integration, and end-to-end tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davieyang](https://clawhub.ai/user/davieyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to create and improve unit and integration tests for Spring Boot, MyBatis, and MySQL projects. It helps generate layered test strategies, Java test examples, test data, coverage checks, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unresolved placeholder GitHub and wget installation paths can lead users to unauthenticated or unintended sources.

Mitigation: Install from ClawHub or use only publisher-verified repositories and pinned releases with checksum or signature verification.

Risk: Bundled scripts can run Maven checks and generate or overwrite project test artifacts.

Mitigation: Run scripts only in disposable or version-controlled test projects and review generated files before committing.

Risk: Example configurations and boundary tests include skip-authentication and memory-exhaustion patterns that can destabilize normal environments if copied directly.

Mitigation: Keep skip-authentication settings limited to test profiles and exclude deliberate memory-exhaustion examples from normal CI pipelines.

## Reference(s):

- [Dependencies](references/dependencies.md)
- [Testing Strategies](references/testing-strategies.md)
- [Exception Patterns](references/exception-patterns.md)
- [Boundary Testing](references/boundary-testing.md)
- [Spring Boot](https://spring.io/projects/spring-boot)
- [Java](https://www.java.com)
- [ClawHub Skill Page](https://clawhub.ai/davieyang/skills/springboot-unit-testing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Java, YAML, SQL, and shell command examples; bundled scripts can generate JSON, HTML, SQL, YAML, and Java files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write project test artifacts; generated files should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, clawhub.yml, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
