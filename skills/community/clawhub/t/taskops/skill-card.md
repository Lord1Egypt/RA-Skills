## Description: <br>
Manage AI-agent work as an execution graph instead of a flat TODO list. Use TaskOps to structure objectives, task decomposition, run readiness, execution logs, exploration, delegation/waiting, EoW closure, validation, summaries, and runner-driven progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmylegendary](https://clawhub.ai/user/jimmylegendary) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use TaskOps to plan, run, validate, and close complex human and AI-agent work with markdown-backed task graphs, run records, blocker/delegation state, summaries, and guarded runner workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git sync and push workflows can affect the selected vault or repository. <br>
Mitigation: Review the target directory for unrelated files or secrets, confirm the remote repository and branch, and use dry-run or bounded runs before unattended synchronization. <br>
Risk: Runner watch and daemon install workflows can start persistent local automation. <br>
Mitigation: Install or start daemons only when persistent automation is intended, set timeouts and retry limits for unattended runs, and monitor status and logs. <br>
Risk: Runner-controlled execution can mutate TaskOps work state. <br>
Mitigation: Validate and summarize the work directory before claiming success, and prefer bounded runner invocations with explicit stop reasons. <br>


## Reference(s): <br>
- [TaskOps on ClawHub](https://clawhub.ai/jimmylegendary/taskops) <br>
- [README](README.md) <br>
- [Core Model](references/core-model.md) <br>
- [Markdown-First Format](references/md-first-format.md) <br>
- [Decomposition Protocol](references/decomposition-protocol.md) <br>
- [Run Readiness](references/run-readiness.md) <br>
- [Legacy Graph Task CLI](references/cli.graph-task.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-producing CLI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and validates file-backed TaskOps work state; runner and daemon workflows may mutate local markdown state, queue ledgers, git repositories, or user-systemd services when invoked.] <br>

## Skill Version(s): <br>
0.5.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
