## Description:

Add meaningful unit tests to existing codebases by finding uncovered behavior, selecting high-value cases, and validating coverage without brittle test inflation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, software maintainers, QA engineers, open-source contributors, and product teams use this skill to plan and add high-value unit tests, regression coverage, focused verification commands, and honest coverage-gap reporting for existing codebases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt an agent to read project code, add or edit test files, and run test commands.

Mitigation: Review planned file changes before applying them and run focused tests before broader or more expensive coverage commands.

Risk: Implicit activation on broad quality requests could be disruptive when the user did not intend test-writing work.

Mitigation: Confirm the testing or coverage goal before editing files when the user request is generic.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-040526)
- [Writing Great Unit Tests: Best and Worst Practices](https://segmentfault.com/a/1190000009709754)
- [What are you looking for when reviewing LLM generated code?](https://news.ycombinator.com/item?id=48538778)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with code patches, test plans, verification commands, and coverage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized test cases, concrete unit test files or patches, focused and broad test commands, coverage movement, and remaining coverage gaps.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
