## Description:

Helps software teams add useful unit tests and improve test coverage for existing codebases through a repeatable, locally practical workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Software maintainers, QA engineers, open-source contributors, and product teams use this skill to plan, add, and verify unit tests that raise coverage while preserving existing behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad testing or quality requests.

Mitigation: Review trigger wording before deployment and narrow invocation policy when the environment requires more precise routing.

Risk: Generated tests or coverage advice may not capture the intended behavior of the target codebase.

Mitigation: Have maintainers review proposed tests, run the project's test suite, and confirm that assertions cover meaningful behavior rather than only increasing line coverage.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-110318)
- [Preventing LLM unit test spam](https://blog.larah.me/test-slop/)
- [Skillgrade: Unit tests for your agent skills](https://github.com/mgechev/skillgrade)
- [Writing Great Unit Tests: Best and Worst Practices](https://segmentfault.com/a/1190000009709754)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text with code, command snippets, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the user's codebase and testing constraints; may include assumptions, limits, and follow-up work.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
