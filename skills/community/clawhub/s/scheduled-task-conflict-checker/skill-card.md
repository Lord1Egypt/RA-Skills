## Description:

Checks proposed LUI/Claw scheduled tasks against existing tasks and account constraints before confirmation, then recommends whether to proceed, reuse, merge, ask for confirmation, block, partially create, or warn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators using LUI/Claw scheduled-task workflows use this skill to normalize a proposed task, compare it with current tasks, and surface duplicate tasks, execution conflicts, permission blocks, and confirmation prompts before task creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unsafe integration guidance in SQL examples.

Mitigation: Require bound parameters in SQL integration examples before broad publishing or production installation.

Risk: The benchmark runner is reported as capable of executing code outside the package.

Mitigation: Constrain benchmark execution to the packaged checker script or avoid running benchmark tools in trusted environments until fixed.

Risk: The skill records local run events by default.

Mitigation: Disable local tracking with SCHEDULED_TASK_CONFLICT_CHECKER_TRACKING=0 or set an approved SCHEDULED_TASK_CONFLICT_CHECKER_TRACK_PATH.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/scheduled-task-conflict-checker)
- [Scheduled task conflict rule matrix](artifact/references/rule-matrix.md)
- [LUI scheduled-task third-party permission SQL checks](artifact/references/permission-sql.md)
- [Benchmark execution report](artifact/benchmarks/lui_conflict_50_cases/benchmark_execution_report.md)
- [Benchmark results](artifact/benchmarks/lui_conflict_50_cases/results/benchmark_results.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [JSON decision payload or Markdown summary with user-facing prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structured proposed_task, existing_tasks, and user_context input; JSON output includes decision, prompt_required, normalized_proposed_task, findings, and user_prompt.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
