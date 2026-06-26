## Description: <br>
Checks proposed LUI/Claw scheduled tasks for duplicates, semantic overlap, execution conflicts, and blocking authorization or platform conditions before task creation is confirmed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to validate scheduled-task requests before creating or updating LUI/Claw tasks. It helps decide whether to proceed, reuse or merge an existing task, ask for confirmation, block creation, partially create, or warn before proceeding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The checker needs structured scheduled-task and shop authorization context for accurate pre-creation decisions. <br>
Mitigation: Provide only the fields needed for conflict and permission checks, and do not include credentials, tokens, full order data, or unnecessary shop-sensitive details. <br>
Risk: Local run logs are written by default for script-level events. <br>
Mitigation: Set SCHEDULED_TASK_CONFLICT_CHECKER_TRACKING=0 to disable local tracking, or set SCHEDULED_TASK_CONFLICT_CHECKER_TRACK_PATH to control the log location. <br>
Risk: Missing or stale task, shop, authorization, platform, or notification context can lead to an incorrect creation recommendation. <br>
Mitigation: Use current structured task and user-context data, and follow the documented conservative decisions for missing context, authorization failures, unsupported platforms, and high-risk write overlaps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/scheduled-task-conflict-checker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/1688aiinfra) <br>
- [Scheduled task conflict rule matrix](artifact/references/rule-matrix.md) <br>
- [Permission SQL reference](artifact/references/permission-sql.md) <br>
- [Benchmark execution report](artifact/benchmarks/lui_conflict_50_cases/benchmark_execution_report.md) <br>
- [Benchmark results](artifact/benchmarks/lui_conflict_50_cases/results/benchmark_results.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON decision payloads and optional Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a decision, prompt requirement, normalized proposed task, findings, and optional user prompt; script input errors use exit code 2.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
