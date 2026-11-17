## Description:

Helps software maintainers, QA engineers, open-source contributors, and product teams add useful unit tests, raise test coverage, and validate changes against regression risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, maintainers, open-source contributors, and product teams use this skill to plan and add practical unit tests, improve coverage, and document verification steps for existing codebases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad testing-related activation wording may invoke the workflow when the user did not explicitly request it.

Mitigation: Prefer explicit invocation when applying this workflow, and confirm the user's testing goal before making recommendations.

Risk: Generated test or coverage changes can encode incorrect assumptions about intended behavior.

Mitigation: Review proposed code changes and run the repository's relevant test and coverage commands before merging.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/unit-test-coverage-helper-234758)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with checklists, code examples, shell commands, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should expose assumptions, limits, validation commands, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
