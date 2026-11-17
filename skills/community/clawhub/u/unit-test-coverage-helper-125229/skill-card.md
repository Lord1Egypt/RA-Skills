## Description:

Helps maintainers and contributors plan, implement, and verify unit tests for software changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to turn requests for added unit tests into a practical plan, checklist, implementation support, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation keywords may activate the skill when the user did not intend unit-test support.

Mitigation: Narrow or disable implicit invocation before installing in environments where accidental activation would be disruptive.

Risk: Generated unit-test plans or code suggestions may miss project-specific behavior or introduce incorrect assertions.

Mitigation: Review suggested changes against the codebase and run the relevant test suite before accepting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-125229)
- [Requirement plan](artifact/references/requirement-plan.md)
- [Source requirement issue](https://github.com/ArpitaVerma16/Voice-Driven-Virtual-Customer-Success-Manager/issues/30)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with optional code snippets and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, implementation steps, verification notes, and follow-up risks.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
