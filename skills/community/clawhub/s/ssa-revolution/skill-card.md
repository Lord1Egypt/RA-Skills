## Description:

Revolution Auto-Evolution orchestrates a coordinator-driven review, execution, and audit loop that helps agents break complex goals into subtasks, iterate through them, and package completed work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate autonomous multi-agent task execution with pre-execution review, implementation, post-execution audit, task-state tracking, and optional packaging of completed work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring autonomous execution can mutate task files and package completed work without continuous operator review.

Mitigation: Run only in a tightly scoped workspace with least-privilege tools, keep monitoring enabled, and require explicit approval for destructive or external actions.

Risk: Task-file content is inserted into reviewer, executor, and auditor prompts and may carry prompt-injection content.

Mitigation: Use trusted task files, validate goals and subtasks before heartbeat processing, and avoid unattended cron use for untrusted tasks.

Risk: Malformed review or audit JSON can fall back to approve or pass behavior.

Mitigation: Require strict JSON validation and fail closed before using the workflow unattended.

Risk: Task and workspace path containment is under-scoped.

Mitigation: Set evolution directories to dedicated locations, validate task filenames and paths, and avoid broad workspace write permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/ssa-revolution)
- [README](README.md)
- [Task example](references/task-example.json)
- [Task schema](config/task-schema.json)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON task files, strict JSON phase outputs, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can mutate workspace task JSON files, emit reviewer/executor/auditor prompts, and package completed tasks into skill directories.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact package.json reports 0.5.7 and SKILL.md reports 0.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
