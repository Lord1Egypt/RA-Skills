## Description:

Automatically generate test documentation for existing skills that have scripts but lack testing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[834948655](https://clawhub.ai/user/834948655)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to create testing documentation for skills that include scripts but lack a TESTING.md file or testing section. It analyzes script behavior and produces test case coverage for normal, edge, and error scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated testing documentation can be incomplete or misleading because the helper emits templates rather than fully verified tests.

Mitigation: Review generated TESTING.md content or SKILL.md testing sections before committing or publishing them.

Risk: The skill may read scripts in the target skill and create or edit testing documentation files.

Mitigation: Inspect the target skill scripts and review any file changes before accepting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/834948655/skills/skill-test-generator)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown documentation with test case tables and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create TESTING.md or add a Testing section to SKILL.md; generated documentation should be reviewed before committing.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
