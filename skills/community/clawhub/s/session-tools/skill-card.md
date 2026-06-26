## Description: <br>
Manage Claude Code sessions by finding IDs, searching history, importing, summarizing, analyzing, classifying, compressing, deleting, repairing, and renaming sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code use this skill to inspect, organize, summarize, recover, compress, move, and delete local session history. It is intended for session maintenance and knowledge extraction workflows where operators can review the selected project and session before taking action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and summarize Claude Code session history that may contain secrets, credentials, private prompts, or sensitive business context. <br>
Mitigation: Review the exact project and session before importing, summarizing, analyzing, syncing, or forwarding session content, and avoid processing sessions that contain sensitive material. <br>
Risk: Some workflows can rewrite, move, compress, or delete local session files. <br>
Mitigation: Back up important sessions and use preview, dry-run, or check-only modes when available before running destructive or bulk cleanup actions. <br>
Risk: The security evidence reports weak safety gates for operations over Claude session history. <br>
Mitigation: Require operator confirmation for the target project/session and for destructive actions such as classify --execute, destroy, repair, compress, or cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/session-tools) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands, MCP tool calls, tables, and summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, summarize, rewrite, move, or delete Claude Code session JSONL files depending on the selected workflow.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
