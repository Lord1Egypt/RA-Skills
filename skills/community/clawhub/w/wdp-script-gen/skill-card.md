## Description:

Helps developers plan, generate, track, and resume long-running or high-volume batch scripts with checkpoints, visible progress, bounded concurrency, retry handling, and failure logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckystar513](https://clawhub.ai/user/luckystar513)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to create or manage resumable batch work across many files or long-running tasks. It is suited for workflows that need explicit planning, checkpoint-based continuation, smoke testing, progress reporting, and auditable failure handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or updates progress, state, log, and checkpoint files in a repository.

Mitigation: Install it only when the agent should manage long-running batch work, and review the work directory contents during use.

Risk: Generated batch scripts may write to manifest-declared output paths.

Mitigation: Review manifests and output directories before full runs, especially in sensitive repositories.

Risk: A full batch run can amplify mistakes across many files or tasks.

Mitigation: Use the documented dry-run, small-limit smoke test, checkpoint, and failure-log workflow before full execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckystar513/skills/wdp-script-gen)
- [wdp-work-mgr recovery protocol](references/protocol.md)
- [8-dimensional batch script design checklist](references/design-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated Python scripts and JSON or JSONL state, progress, checkpoint, and failure-log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scoped work/ planning and progress files, plus resumable batch-script helpers that write to manifest-declared output paths.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
