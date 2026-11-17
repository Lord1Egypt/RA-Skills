## Description:

Helps maintainers and QA teams plan, implement, and verify useful unit tests that raise coverage for existing codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, software maintainers, QA engineers, open-source contributors, and product teams use this skill to turn unit-test coverage requests into practical plans, code or workflow guidance, checklists, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to be invoked for general testing or quality requests.

Mitigation: Confirm the request is specifically about unit tests, test coverage, regression risk, or test verification before applying the workflow.

Risk: Generated unit-test plans or code may not accurately reflect the target codebase behavior.

Mitigation: Review proposed tests against the implementation and run the stated verification commands before relying on coverage changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-080414)
- [Requirement Plan](references/requirement-plan.md)
- [Preventing LLM Unit Test Spam](https://blog.larah.me/test-slop/)
- [Skillgrade: Unit Tests for Agent Skills](https://github.com/mgechev/skillgrade)
- [Shipwright Code Quality Agent Issue](https://github.com/sethdford/shipwright/issues/785)
- [Shipwright Pipeline Cache Issue](https://github.com/sethdford/shipwright/issues/787)
- [Codex Dynamic Workflows Issue](https://github.com/kedarkolluri/codex/issues/1)
- [Codex Context Bounds Issue](https://github.com/kedarkolluri/codex/issues/59)
- [Polis Local Model Backend Issue](https://github.com/PSyron/polis/issues/43)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with optional code blocks, command snippets, checklists, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, implementation steps, verification commands, remaining risks, and follow-up work.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
