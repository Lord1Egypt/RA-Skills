## Description:

Self Driven helps an agent choose, execute, evaluate, record, and report tasks in a self-directed loop without waiting for direct user prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a traceable autonomous task loop that reads prior progress, selects a task, performs work, self-assesses, and records the result. It is intended for users who deliberately want persistent or scheduled self-directed agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage autonomous, scheduled, or persistent agent work without clear approval boundaries.

Mitigation: Require explicit approval for file changes, shell or tool use, network access, credential use, and third-party actions before enabling the loop.

Risk: Task memory and execution logs could spread beyond the intended workspace or persist longer than expected.

Mitigation: Keep memory/self-driven files in a dedicated scoped directory with clear retention and review practices.

Risk: Unattended cron execution may let the agent continue acting after the operator has lost context.

Mitigation: Avoid unattended cron execution unless the runtime is tightly sandboxed and reviewed between runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adminlove520/skills/self-driven)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance, task records, execution logs, status reports, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update scoped memory files such as memory/self-driven/tasks.md and memory/self-driven/log.md when file changes are permitted.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
