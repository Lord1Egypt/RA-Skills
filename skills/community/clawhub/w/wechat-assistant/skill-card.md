## Description: <br>
Wechat Assistant helps agents capture WeChat desktop chat records on Windows, analyze conversations, manage a reply knowledge base, generate reviewed replies, and create charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luemery](https://clawhub.ai/user/luemery) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to analyze authorized WeChat desktop conversations, extract needs and relationship signals, build a local reply knowledge base, and draft replies that require review before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private WeChat chat content and stores exported messages, reply history, and knowledge-base data locally. <br>
Mitigation: Use it only on chats you are authorized to process, choose narrow contact and message-count scopes, store exports in protected folders, and delete reply_history.json and kb_data.json when no longer needed. <br>
Risk: Local UI automation can act against an already logged-in WeChat desktop session. <br>
Mitigation: Install and run the skill only when local automation access is acceptable, keep the intended chat window visible, and review each generated reply before any send action. <br>


## Reference(s): <br>
- [Format specification](references/format_spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/luemery/wechat-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or PNG file outputs from the bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on Windows with WeChat desktop visible and logged in; reply generation creates review records before any send step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
