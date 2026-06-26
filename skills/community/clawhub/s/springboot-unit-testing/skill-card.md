## Description: <br>
Helps developers create layered unit and integration tests for Spring Boot, MyBatis, and MySQL projects, including normal-flow, exception, boundary, coverage, and test-data workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davieyang](https://clawhub.ai/user/davieyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, generate, and review Spring Boot test suites across Mapper, Service, Controller, and integration layers. It is aimed at projects that need practical JUnit 5, Mockito, H2, Testcontainers, coverage, test-data, and boundary-testing guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL and database examples may modify tables or seed data if run against a persistent database. <br>
Mitigation: Run generated SQL only in disposable test databases such as H2, Testcontainers, or an isolated test schema. <br>
Risk: Local helper scripts run Maven commands and write generated test-data and report files into the target project. <br>
Mitigation: Review scripts and run them only in trusted project checkouts with source control available for reviewing generated changes. <br>
Risk: The release license evidence is inconsistent between server metadata and artifact metadata. <br>
Mitigation: Confirm the authoritative license before publishing or relying on redistribution terms. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/davieyang/springboot-unit-testing) <br>
- [Boundary testing guide](references/boundary-testing.md) <br>
- [Testing dependencies guide](references/dependencies.md) <br>
- [Exception testing patterns](references/exception-patterns.md) <br>
- [Testing strategies guide](references/testing-strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Java, YAML, SQL, Maven, and shell snippets; helper scripts can generate SQL, JSON, YAML, Java, JSON report, and HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include test coverage thresholds, generated test data, and local project report artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, and clawhub.yml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
