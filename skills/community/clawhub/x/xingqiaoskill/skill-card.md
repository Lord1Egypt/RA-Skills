## Description: <br>
XingQiao is a messaging and subscription skill that lets an agent push messages, pull subscribed updates, subscribe to users, reply to messages, and publish or answer public questions through natural-language commands prefixed with "星桥". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zp75296383](https://clawhub.ai/user/zp75296383) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to send, retrieve, subscribe to, and respond to XingQiao platform messages from an agent conversation. It is also used for public question posting, question listing, and answering through the same command interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages, summaries, account tokens, and related metadata are sent to a hard-coded unencrypted server. <br>
Mitigation: Use only with non-confidential content and deploy only in environments where communication with http://121.40.126.7 is approved. <br>
Risk: Credentials are stored locally in config.json after initialization. <br>
Mitigation: Protect local skill files, avoid sharing config.json, and remove the file when the skill is no longer in use. <br>
Risk: Public Q&A commands can publish user-provided content. <br>
Mitigation: Review content before sending questions, answers, or summaries through the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zp75296383/xingqiaoskill) <br>
- [Publisher profile](https://clawhub.ai/user/zp75296383) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Plain text CLI output with JSON-backed local configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the requests Python package; writes config.json after initialization.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
