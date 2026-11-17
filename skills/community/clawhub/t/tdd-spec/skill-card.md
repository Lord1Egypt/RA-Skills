## Description:

Guides agents through SPEC-approved test-driven development by mapping requirements and acceptance criteria to red-green-refactor implementation slices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to implement approved SPEC SDD features or bug fixes one vertical slice at a time, with each test mapped to a numbered requirement or acceptance criterion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to modify project code and tests during implementation work.

Mitigation: Use it only with an approved SPEC, keep each change scoped to one requirement or acceptance criterion, and run the relevant tests, lint, type checks, and validation commands after each slice.

Risk: The skill expects user-facing questions and recommendations in Portuguese (pt-BR), which may not fit every project or team workflow.

Mitigation: Confirm the language expectation is acceptable before using the skill in a user-facing workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/tdd-spec)
- [Publisher profile](https://clawhub.ai/user/afonsoft)
- [Source repository](https://github.com/afonsoft/skills)
- [tests.md](tests.md)
- [mocking.md](mocking.md)
- [refactoring.md](refactoring.md)
- [deep-modules.md](deep-modules.md)
- [interface-design.md](interface-design.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with code, test, command, and progress-report suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing questions and recommendations are expected in Portuguese (pt-BR); work proceeds one SPEC-derived slice at a time.]

## Skill Version(s):

1.0.0 (source: server release, metadata, and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
