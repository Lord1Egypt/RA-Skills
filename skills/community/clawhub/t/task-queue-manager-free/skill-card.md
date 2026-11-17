## Description: <br>
Provides persistent local task queue guidance for recoverable, idempotent batch work managed by an AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to plan and run local file-backed queues for batch processing, progress tracking, failure handling, and resumable task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queued payloads, results, and failed-task details are stored on disk under workspace/tasks and may be retained after processing. <br>
Mitigation: Avoid placing secrets, regulated personal data, or confidential business records in queue payloads unless local retention is acceptable. <br>
Risk: The skill can propose shell commands and example code for queue operations, including workflows that may touch databases or external APIs. <br>
Mitigation: Review generated commands and code before execution, especially before writes to databases, external APIs, or shared workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/task-queue-manager-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash and Python code snippets; local JSON and JSONL queue state files may be created under workspace/tasks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include task status, progress, retry guidance, and file-backed queue records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
