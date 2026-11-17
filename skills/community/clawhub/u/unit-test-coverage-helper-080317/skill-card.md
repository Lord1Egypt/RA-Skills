## Description:

Helps software maintainers, QA engineers, open-source contributors, and product teams create useful unit tests, raise test coverage, and verify changes against existing behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, QA engineers, open-source contributors, and product teams use this skill to plan and implement repeatable unit-test coverage improvements for existing codebases. It helps clarify goals, propose local-hardware-friendly implementation steps, produce checklists or code guidance, and identify verification commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad testing-related trigger language may route requests to this skill in environments with overlapping software-engineering skills.

Mitigation: Review or narrow implicit invocation triggers before deployment when precise routing matters.

Risk: Generated testing guidance or proposed code changes could be incomplete or misaligned with the target codebase.

Mitigation: Review proposed tests and run the recommended verification commands before accepting changes.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Preventing LLM unit test spam](https://blog.larah.me/test-slop/)
- [Skillgrade: "Unit tests" for your agent skills](https://github.com/mgechev/skillgrade)
- [Writing Great Unit Tests: Best and Worst Practices](https://segmentfault.com/a/1190000009709754)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with checklists, implementation guidance, code snippets, and verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, limits, validation steps, and remaining risks when helpful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
