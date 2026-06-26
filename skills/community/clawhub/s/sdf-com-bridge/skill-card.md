## Description: <br>
SDF COM Bridge connects SDF COM chatrooms with Feishu or Lark, relaying messages, translating between English and Chinese, and forwarding supported COM commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YKaiXu](https://clawhub.ai/user/YKaiXu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to bridge an SDF Public Access UNIX System COM room with Feishu or Lark so chat participants can exchange translated messages and supported COM commands across systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge mirrors and translates chat content between SDF COM and Feishu or Lark, which may expose conversations to a broader audience than participants expect. <br>
Mitigation: Use it only in rooms and Feishu/Lark chats where all participants expect mirroring and translation. <br>
Risk: The bridge can use an existing SSH session for the configured SDF account. <br>
Mitigation: Run it with a dedicated low-privilege SDF account and keep the SSH socket scoped to that account. <br>
Risk: Translation queues, translation results, state files, and bridge logs can temporarily retain chat text or connection details on disk. <br>
Mitigation: Avoid sensitive conversations and periodically clear the local translation queue, result files, state files, and bridge logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YKaiXu/sdf-com-bridge) <br>
- [Server-resolved publisher profile](https://clawhub.ai/user/YKaiXu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local translation queue, translation result, bridge state, and bridge log files during use.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
