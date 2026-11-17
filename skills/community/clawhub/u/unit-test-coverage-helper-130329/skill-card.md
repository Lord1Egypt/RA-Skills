## Description:

Helps maintainers, QA engineers, open-source contributors, and product teams add useful unit tests, improve coverage, and verify behavior in existing codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, software maintainers, QA engineers, open-source contributors, and product teams use this skill to plan and produce practical unit-test coverage improvements for existing codebases. It helps clarify constraints, generate tailored workflows or code-change support, and include verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad testing and quality triggers plus implicit invocation may activate the skill for general testing requests.

Mitigation: Use explicit invocation with $unit-test-coverage-helper when unit-test coverage help is intended, and review proposed test changes before applying them.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Preventing LLM unit test spam](https://blog.larah.me/test-slop/)
- [Skillgrade: "Unit tests" for your agent skills](https://github.com/mgechev/skillgrade)
- [test: add end-to-end GitHub workflow contract coverage](https://github.com/RapierCraftStudios/ForgeDock-CLI/issues/4)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-130329)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, implementation steps, reusable checklists, and verification notes.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
