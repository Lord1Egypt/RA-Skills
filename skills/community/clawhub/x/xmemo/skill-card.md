## Description: <br>
Persistent user-owned memory for agents with standalone runtime execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmemo](https://clawhub.ai/user/xmemo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use XMemo to let agents recall, search, update, and preserve durable user-owned memory across sessions, including handoff state, TODOs, troubleshooting context, and expense records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected memory, task-state, TODO, or expense content may be sent to and stored by the hosted XMemo service. <br>
Mitigation: Use the skill only for content appropriate for remote storage, and do not store secrets, credentials, private customer data, or sensitive internal context unless the service privacy and retention terms have been reviewed. <br>
Risk: Credential handling can expose XMemo tokens if users paste them into chat, logs, screenshots, repositories, or command history. <br>
Mitigation: Use the login flow or stdin-based credential import, keep credentials out of project files and shared logs, and run the diagnostic commands when authentication fails. <br>


## Reference(s): <br>
- [XMemo Skill Operations](references/operations.md) <br>
- [XMemo Skill Troubleshooting](references/troubleshooting.md) <br>
- [XMemo hosted service](https://xmemo.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the bundled script can return plain text or JSON with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Standalone Node.js runtime commands call the hosted XMemo service and require a valid credential for authenticated memory operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
