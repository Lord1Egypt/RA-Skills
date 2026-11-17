## Description:

Helps software teams plan, add, and validate useful unit tests and coverage improvements for existing codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Software maintainers, QA engineers, open-source contributors, and product teams use this skill to create practical unit-test coverage plans, checklists, code-oriented next steps, and validation notes for existing codebases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad testing-related prompts.

Mitigation: Confirm the user's testing or coverage goal before applying the workflow, and keep assumptions visible in the response.

Risk: Coverage guidance can be misleading if it is not checked against the target codebase and test framework.

Mitigation: Inspect the local project constraints and include concrete verification commands or review steps when code or configuration changes are proposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-120435)
- [Requirement Plan](artifact/references/requirement-plan.md)
- [[aw] No-Op Runs](https://github.com/github/gh-aw/issues/39849)
- [test: add dedicated test coverage for ReadmeHealthBreakdown component](https://github.com/JhaSourav07/commitpulse/issues/6683)
- [How Small Can a C++ Unit Test Framework Be?](https://freshsources.com/code-capsules/test-part1/)
- [What are you looking for when reviewing LLM generated code?](https://news.ycombinator.com/item?id=48538778)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code blocks, commands, checklists, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the user's codebase context; may include assumptions, limits, and follow-up work.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
