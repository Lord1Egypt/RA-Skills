## Description: <br>
Weixin Task Workbench helps an agent manage multiple long-running tasks from one WeChat/OpenClaw conversation by routing each task to its own session and maintaining task state, summaries, closure, and archival status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnhan98](https://clawhub.ai/user/shawnhan98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WeChat/OpenClaw users and operators use this skill to keep several parallel work items isolated while staying in a single chat. It supports task creation, listing, switching, continuation, summarization, closure, archival, and troubleshooting status views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task registry data can be silently mixed between WeChat/OpenClaw account folders. <br>
Mitigation: Review before installing and change registry handling so one account cannot import, merge, or copy task records from another account without explicit user action. <br>
Risk: Session keys and full registry paths may be exposed in normal status output. <br>
Mitigation: Mask session keys and full registry paths by default, exposing them only when the user is intentionally troubleshooting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shawnhan98/weixin-task-workbench) <br>
- [Implementation notes](references/implementation.md) <br>
- [Workbench protocol](references/protocol.md) <br>
- [Test matrix](references/test-matrix.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style task responses with inline command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and host session tools for spawning, sending to, and reading task sessions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
