## Description:

Use when you have a spec or requirements for a multi-step task, before touching code - guides writing comprehensive implementation plans with bite-sized tasks, TDD, and DRY/YAGNI principles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to turn a multi-step implementation spec into a detailed Markdown plan before code changes begin. The plan is expected to include file responsibilities, small test-driven tasks, concrete commands, commits, and handoff options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce implementation plans that include git branch, merge, commit, or subagent workflow steps.

Mitigation: Review the generated plan before allowing follow-on implementation, especially version-control and subagent steps.

Risk: The operating instructions are written in Chinese, which may be unsuitable for teams or agents that require English-language instructions.

Mitigation: Install only where Chinese-language operating instructions are acceptable, or translate and review the skill before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/superpowers-writing-plans)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown plan with task checklists and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans are saved under docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md and should be reviewed before implementation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
