## Description: <br>
Maintains persistent per-task files so OpenClaw agents can preserve task context across session resets, compaction, and channel switches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanzhang1128](https://clawhub.ai/user/dylanzhang1128) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep task status, decisions, todos, and handoff context available across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent plaintext task notes may contain sensitive project details if users add them. <br>
Mitigation: Review the tasks directory periodically and avoid storing passwords, tokens, private account details, sensitive links, or confidential configuration values. <br>


## Reference(s): <br>
- [Task Tracker Reference](references/DESIGN.md) <br>
- [ClawHub skill page](https://clawhub.ai/dylanzhang1128/session-task-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown task files and concise text status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and maintains plaintext task notes under the workspace tasks directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
