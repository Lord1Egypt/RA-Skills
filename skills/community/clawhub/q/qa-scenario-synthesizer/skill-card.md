## Description:

Generates structured QA scenario sets from requirements, covering main flows, exceptions, cross-platform behavior, invalid inputs, recovery, and priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, developers, and product reviewers use this skill to turn requirements, user flows, and constraints into reviewable test-scenario drafts and execution checklists. It is suited for test design, integration preparation, and acceptance coverage planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scenarios may omit important paths or imply more test coverage than was actually executed.

Mitigation: Treat outputs as reviewable QA design drafts and have a human reviewer confirm coverage before using them for release decisions.

Risk: Input requirements may contain sensitive business, user, or compliance details.

Mitigation: Redact sensitive requirements before use and provide only files intended to be shared with the skill.

Risk: The artifact contains inactive audit modes in addition to the default scenario-generation mode.

Mitigation: Keep the provided specification in its default structured scenario mode unless local scanning behavior is explicitly desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/qa-scenario-synthesizer)
- [README](artifact/README.md)
- [Scenario Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)
- [Smoke Test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown by default, with optional JSON report output from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize reviewable drafts, missing-information lists, priorities, and next-step checklists.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
