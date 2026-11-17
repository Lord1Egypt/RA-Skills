## Description:

Helps software teams plan, add, and verify useful unit tests to improve coverage in existing codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, QA engineers, and product teams use this skill to turn coverage gaps into practical unit-test plans, implementation steps, and verification notes for existing codebases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms may cause the skill to be selected for general testing or quality prompts.

Mitigation: Review the implicit invocation policy before installation if the deployment requires explicit skill selection.

Risk: Generated test plans or code changes may miss project-specific behavior or create shallow coverage.

Mitigation: Review proposed tests against the codebase's intended behavior and run the relevant unit-test and coverage commands before relying on the result.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-200354)
- [Preventing LLM unit test spam](https://blog.larah.me/test-slop/)
- [Skillgrade: Unit tests for your agent skills](https://github.com/mgechev/skillgrade)
- [Coverage gap issue](https://github.com/kubestellar/console/issues/21025)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code, shell command, and checklist blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, verification steps, remaining risks, and follow-up work when useful.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
