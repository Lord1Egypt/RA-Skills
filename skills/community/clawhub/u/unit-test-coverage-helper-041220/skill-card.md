## Description:

Helps maintainers, QA engineers, contributors, and product teams add useful unit tests and improve coverage for existing codebases through repeatable workflows, checklists, implementation support, and verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, open-source contributors, and product teams use this skill to plan and add practical unit tests, raise coverage, and reduce regression risk in existing codebases. It turns testing requests into scoped implementation steps, reusable checklists, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad testing-related trigger language may select the skill for requests where the user needs a narrower framework-specific testing workflow.

Mitigation: Confirm the user's target language, framework, constraints, and success criteria before proposing or changing tests when those details materially affect the result.

Risk: Generated unit test plans or code changes can encode incorrect assumptions about existing behavior.

Mitigation: Inspect the relevant code and run repository-native verification commands before presenting the result as ready to use.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code, shell command, checklist, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's codebase and include assumptions, validation steps, and remaining risks when relevant.]

## Skill Version(s):

0.20260729.110214 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
