## Description: <br>
Search and analyze your own session logs (older/parent conversations) using jq. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to locate and summarize prior OpenClaw conversations stored as local JSONL session logs when a user asks about older or parent chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface sensitive local conversation history from OpenClaw session logs. <br>
Mitigation: Use narrow searches, inspect excerpts before sharing, and avoid displaying secrets or unrelated private history. <br>
Risk: Command examples read local session files and rely on the correct agent ID and session path. <br>
Mitigation: Verify the target agent and session directory before running searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1yihui/yihui-session-logs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with jq, rg, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local access to OpenClaw session logs and jq; rg is used for text search.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
