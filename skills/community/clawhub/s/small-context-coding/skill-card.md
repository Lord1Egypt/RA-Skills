## Description:

Efficient coding workflow for small-context models working on medium or large codebases. Use when the user wants to develop, debug, refactor, or analyze code with limited context windows, when tasks should be split into smaller verified steps, when sub-agents may help isolate work, or when long coding sessions need plan files, checkpoints, and strict context discipline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ambitioncn](https://clawhub.ai/user/ambitioncn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to manage medium or large software tasks with limited context by keeping plans, todos, checkpoints, and verification choices in local files. It also helps split isolated investigation, implementation, or test work into concise sub-agent briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts can create planning notes and sub-agent brief files inside a target repository.

Mitigation: Run the scripts only in repositories where notes/<task-slug>/ files are acceptable, and review generated notes before relying on them.

Risk: Sub-agent briefs may narrow the scope too much or omit important project context.

Mitigation: Review each generated brief for scope, verification command, and remaining risks before delegating work.

## Reference(s):

- [Usage Guide](references/usage-guide.md)
- [Verification Defaults](references/verification-defaults.md)
- [Sub-agent Patterns](references/subagent-patterns.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated Markdown note files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local notes/<task-slug>/ planning files and notes/<task-slug>/subagents/*.brief.md files when helper scripts are run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
