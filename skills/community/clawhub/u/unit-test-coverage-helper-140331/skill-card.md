## Description:

Helps software maintainers, QA engineers, open-source contributors, and product teams plan, write, and verify useful unit tests and test coverage improvements for existing codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, maintainers, and product teams use this skill to turn testing or coverage requests into practical plans, code changes, checklists, and verification notes. It is intended for existing codebases where teams need confidence that changes do not break current behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad testing or quality prompts may activate this skill when a different testing workflow was intended.

Mitigation: Explicitly name the desired skill or clarify the testing scope before invocation.

Risk: Generated testing plans or code changes may not match the target repository's behavior.

Mitigation: Review proposed changes and run the repository's unit test and coverage commands before merging.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Unit Test Coverage Helper on ClawHub](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-140331)
- [Skillgrade: Unit tests for agent skills](https://github.com/mgechev/skillgrade)
- [Writing Great Unit Tests: Best and Worst Practices](https://segmentfault.com/a/1190000009709754)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code, shell command, checklist, and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, limits, verification notes, and follow-up work when useful.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
