## Description:

Unified AI workflow with persistent memory, TDD execution, and 15 productivity skills. Use when starting any coding project or when you need planning, execution, debugging, or code review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mok888](https://clawhub.ai/user/mok888)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to organize planning, implementation, debugging, code review, branch completion, and verification workflows around persistent project memory files and TDD-oriented execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may broadly steer an agent's behavior across planning, execution, debugging, and review tasks.

Mitigation: Use the skill only when its workflow is desired, review generated plans before execution, and keep human approval gates for code changes and branch completion.

Risk: Persistent memory and session catch-up behavior may surface private prior-session transcript content into future prompts or shared logs.

Mitigation: Avoid using session catch-up on sensitive projects, review recovered content before sharing it, and disable or require approval for session-catchup.py when privacy matters.

Risk: Bundled hooks and scripts may run locally and write project memory files.

Mitigation: Review hook files before enabling them, run in a controlled workspace, and require approval for hook execution on sensitive repositories.

## Reference(s):

- [Superpower with Files ClawHub Listing](https://clawhub.ai/mok888/skills/superpower-with-files)
- [README](README.md)
- [Skill Definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates, shell commands, and implementation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent planning files such as task_plan.md, progress.md, and findings.md in a project workspace.]

## Skill Version(s):

2.20.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
