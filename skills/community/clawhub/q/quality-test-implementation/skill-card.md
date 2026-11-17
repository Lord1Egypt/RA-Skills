## Description:

Use when raising code quality or test coverage across a .NET, Java, or Python repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to stabilize .NET, Java, or Python repositories by reducing static-analysis warnings, improving test coverage, fixing security findings, updating documentation, and preparing a technical summary for manual pull request creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad quality, dependency, test, documentation, and commit changes across a repository.

Mitigation: Run it on a feature branch in a disposable or isolated development environment and review all generated changes before merge.

Risk: Coverage and security workflows may invoke project tooling and optional package or tool installation paths.

Mitigation: Pin or locally scope optional pip and .NET tool installs where practical, and run the workflow only in repositories where these commands are expected.

## Reference(s):

- [.NET test coverage guidance](references/coverage-dotnet.md)
- [Java test coverage guidance](references/coverage-java.md)
- [Python test coverage guidance](references/coverage-python.md)
- [Coverage dispatcher script](references/run-coverage.sh)
- [Source repository](https://github.com/afonsoft/skills)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, repository file changes, coverage reports, and a technical summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a feature branch, update tests, documentation, dependency configuration, README, CHANGELOG, and commit metadata; it does not automatically open a pull request.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata; SKILL.md metadata.version is 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
