## Description:

Use when executing implementation plans with independent tasks in the current session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[user-wangjun](https://clawhub.ai/user/user-wangjun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to execute implementation plans whose tasks are mostly independent by delegating each task to a fresh subagent. It keeps implementation, spec compliance review, and code quality review in the current session before moving to the next task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow delegates coding work to subagents and may create commits in the repository.

Mitigation: Review generated commits, changed files, and test results before merging or deploying the work.

Risk: Delegated implementation and review can still produce incorrect or misleading guidance or code.

Mitigation: Keep the spec compliance and code quality review gates mandatory, and inspect reviewer findings before proceeding to the next task.

Risk: Some escalation and help text appears in Chinese and may not match every team's operating language.

Mitigation: Adapt the prompt templates to the team's language and escalation policy before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/user-wangjun/skills/subagent-driven-dev)
- [Implementer prompt template](artifact/implementer-prompt.md)
- [Spec compliance reviewer prompt template](artifact/spec-reviewer-prompt.md)
- [Code quality reviewer prompt template](artifact/code-quality-reviewer-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with prompt templates, implementation reports, test results, and review findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in repository changes and commits proposed by delegated coding subagents.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
