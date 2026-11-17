## Description:

Helps software maintainers, QA engineers, contributors, and product teams add useful unit tests and improve coverage for existing codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, QA engineers, open-source contributors, and product teams use this skill to plan, create, and validate unit tests that improve coverage and protect existing behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad testing or quality-related requests when several development skills are installed.

Mitigation: Prefer explicit invocation when the user wants this specific unit-test coverage workflow.

Risk: Generated test plans or code changes may miss project-specific behavior or add low-value tests.

Mitigation: Review proposed tests against existing behavior and run the project's test suite or coverage command before adopting changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-230850)
- [Requirement Plan](artifact/references/requirement-plan.md)
- [Production test coverage issue](https://github.com/openpacketcore/openpacketcore-sdk/issues/143)
- [AWS CDK circuit breaker testing issue](https://github.com/aws/aws-cdk/issues/38244)
- [Preventing LLM unit test spam](https://blog.larah.me/test-slop/)
- [Skillgrade unit-test evaluation reference](https://github.com/mgechev/skillgrade)
- [Writing Great Unit Tests](https://segmentfault.com/a/1190000009709754)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional code blocks, shell commands, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include assumptions, implementation steps, tests to add, coverage commands, residual risks, and next-step guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
