## Description:

Helps software teams add useful unit tests, improve test coverage, and create practical verification workflows for existing codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Software maintainers, QA engineers, open-source contributors, and product teams use this skill to plan, implement, and verify unit-test coverage improvements without needing to read the original demand evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked for broad testing or quality requests where unit-test coverage help is not the best fit.

Mitigation: Prefer explicit invocation when unit-test or regression-test support is wanted, and confirm scope before applying suggested changes.

Risk: Suggested tests or code changes may fail to preserve intended behavior if accepted without review.

Mitigation: Review proposed changes and run the relevant local test or coverage commands before merging.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-020416)
- [Preventing LLM unit test spam](https://blog.larah.me/test-slop/)
- [Skillgrade: Unit tests for your agent skills](https://github.com/mgechev/skillgrade)
- [Test failure: System.Security.Cryptography.Tests](https://github.com/dotnet/runtime/issues/130441)
- [ci: commit-metadata gates never run on dev pushes, and pass vacuously on workflow_dispatch](https://github.com/bsikar/ra8-firmware/issues/357)
- [Roadmap: complete Neo C# contract compatibility diagnostics](https://github.com/neo-project/neo-devpack-dotnet/issues/1841)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code snippets, shell commands, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's codebase context and should include assumptions, limits, and validation steps when helpful.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
