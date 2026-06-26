## Description: <br>
Wechat Automation helps an agent automate Windows PC WeChat tasks such as sending messages, bulk messaging, reading chat history, listing contacts, auto-replying, and managing Moments through pywechat127. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[838997125](https://clawhub.ai/user/838997125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to operate a live Windows PC WeChat session from an agent, including message sending, batch sends, contact lookup, chat-history reads, and environment checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a live WeChat account and send messages, including bulk sends, from the user's desktop session. <br>
Mitigation: Require explicit manual confirmation for every send, bulk send, file transfer, auto-reply, and Moments action, and avoid promotional or spam-like use. <br>
Risk: The skill can read private chat history and contact information and print results to the terminal. <br>
Mitigation: Confirm each contact listing or chat-history read before execution and keep chat and contact output out of shared logs, transcripts, and terminals. <br>
Risk: Generated .bat files run WeChat automation outside the agent sandbox in the user's real Windows desktop session. <br>
Mitigation: Inspect generated .bat files before running them and execute them only in a trusted local session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/838997125/zyq-wechat-automation) <br>
- [pywechat127 PyPI](https://pypi.org/project/pywechat127/) <br>
- [pywechat GitHub](https://github.com/Hello-Mr-Crab/pywechat) <br>
- [FAQ](references/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; scripts may print WeChat contact, message, and execution status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, a logged-in WeChat desktop session, and pywechat127-related dependencies.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
