## Description: <br>
Controls a local Windows WeChat client with Python to log in, send text messages, list recent chats, and report unread message counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ltf13133-wq](https://clawhub.ai/user/ltf13133-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local automation users can use this skill to operate a personal Windows WeChat session from an agent workflow, including sending messages and checking recent chat or unread-count status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A cached WeChat login can persist agent access to the user's account across runs. <br>
Mitigation: Install only on a trusted personal machine, avoid shared or synced environments, and delete loginInfo.pkl when persistent access is no longer needed. <br>
Risk: The skill can send messages and read chat metadata without built-in confirmation or tight scoping. <br>
Mitigation: Verify recipient names and message text before invoking send, and use the skill only with accounts and chats the operator is comfortable exposing to the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ltf13133-wq/wechat-control) <br>
- [Publisher profile](https://clawhub.ai/user/ltf13133-wq) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [CLI text output with JSON arrays for chat listings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python dependencies and a local Windows WeChat session; login state may be cached by itchat.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata; artifact manifest lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
