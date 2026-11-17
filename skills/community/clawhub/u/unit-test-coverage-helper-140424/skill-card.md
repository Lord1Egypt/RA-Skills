## Description:

Helps developers, maintainers, and QA teams add useful unit tests, improve coverage, and verify that changes do not break existing behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, software maintainers, QA engineers, open-source contributors, and product teams use this skill to turn testing and coverage requests into scoped workflows, concrete test artifacts or code changes, and verification steps for existing codebases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad testing and quality activation wording may make the skill noisier than a narrowly scoped unit-test helper.

Mitigation: Use explicit task wording and review whether the skill is appropriate before applying it to broad quality requests.

Risk: Generated tests, code changes, and shell commands may be incorrect or unsuitable for a repository.

Mitigation: Review generated artifacts and commands before applying them, then run the relevant test suite or coverage command.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Preventing LLM Unit Test Spam](https://blog.larah.me/test-slop/)
- [Skillgrade: Unit Tests for Agent Skills](https://github.com/mgechev/skillgrade)
- [Writing Great Unit Tests: Best and Worst Practices](https://segmentfault.com/a/1190000009709754)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, often with code snippets, shell commands, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should expose assumptions, limits, required inputs, and remaining risks when helpful.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
