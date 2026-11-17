## Description:

Helps software teams add useful unit tests, raise test coverage, and verify changes against existing behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, maintainers, and product teams use this skill to plan, implement, and validate unit tests and coverage improvements for existing codebases. It can produce tailored guidance, reusable workflows, checklists, code changes, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked broadly for testing-related requests because implicit invocation is enabled and trigger terms are general.

Mitigation: Review activation behavior during deployment and narrow trigger wording if the skill routes too broadly.

Risk: Testing and coverage guidance can be incomplete or misleading if it is not checked against the target codebase and its test runner.

Mitigation: Require generated plans or code changes to include concrete verification commands and list assumptions, limits, and remaining risks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-120606)
- [Requirement Plan](references/requirement-plan.md)
- [Hydraflow watchdog issue](https://github.com/T-rav/hydraflow/issues/9455)
- [Hydraflow caretaker loop issue](https://github.com/T-rav/hydraflow/issues/9454)
- [Angular Jasmine unit test discussion](https://news.ycombinator.com/item?id=48375380)
- [LLM generated code review discussion](https://news.ycombinator.com/item?id=48538778)
- [Writing Great Unit Tests](https://segmentfault.com/a/1190000009709754)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, constraints, remaining risks, and follow-up work when relevant.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
