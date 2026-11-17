## Description:

Manage AI-agent work as an execution graph instead of a flat TODO list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmylegendary](https://clawhub.ai/user/jimmylegendary)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use TaskOps to structure complex agentic work as markdown-backed work graphs with explicit decomposition, execution logs, blockers, delegation, validation, summaries, and closure evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent execution and daemon installation can continue operating on local work graphs beyond a single interactive step.

Mitigation: Use daemon install/start only after reviewing the target work directory, service name, runtime, timeout, retry, and service lifetime; prefer bounded dry-run or single-step execution for initial validation.

Risk: Git sync and file mutation paths can change local markdown state or push vault changes to a remote branch.

Mitigation: Review the exact work directory, git diff, repository URL, and branch before enabling vault auto-sync, watch-sync, or git-sync.

Risk: Progress reporting through openclaw-chat-inject may expose run status to a configured chat session.

Mitigation: Avoid openclaw-chat-inject until the report sink, master session key handling, and intended recipient session have been reviewed.

Risk: Legacy graph_task.py migration tooling can be misapplied to untrusted graph IDs or forceful export flows.

Mitigation: Use the current TaskOps CLI for normal validation and summaries; run legacy graph_task.py only for explicit migration work in a contained workspace.

## Reference(s):

- [TaskOps core model](references/core-model.md)
- [TaskOps md-first format](references/md-first-format.md)
- [TaskOps Decomposition Protocol](references/decomposition-protocol.md)
- [Run Readiness](references/run-readiness.md)
- [TaskOps ClawHub release page](https://clawhub.ai/jimmylegendary/skills/taskops)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON-oriented CLI output, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update markdown work-graph files, run logs, summaries, SQLite queue projections, git-sync metadata, and local daemon/service configuration when the documented CLI paths are used.]

## Skill Version(s):

0.5.4 (source: server release metadata, released 2026-06-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
