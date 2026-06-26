## Description: <br>
Durable queue-task helper for resumable, idempotent batch jobs in task-father task folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moodykong](https://clawhub.ai/user/moodykong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to initialize and manage local, file-backed queue state for long-running batch tasks that need resumable progress, append-only logs, and simple lock handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The task slug can escape the intended task folder and write queue state files elsewhere on disk. <br>
Mitigation: Use simple slug names without slashes or '..', set WORKSPACE_DIR to a controlled directory, and patch slug validation before shared or automated use. <br>
Risk: Running the helper with broad filesystem privileges can increase the impact of unintended file writes. <br>
Mitigation: Run without elevated privileges and restrict configuration to a workspace directory intended for queue state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moodykong/queue-task) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local queue files including queue.jsonl, progress.json, done.jsonl, failed.jsonl, lock.json, TASK.md, and TODOS.md.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
