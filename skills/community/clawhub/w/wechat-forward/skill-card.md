## Description: <br>
For explicit user requests, this skill prepares recent chat content and sends it to the user's own WeChat account through the wxclawbot CLI for mobile viewing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidchyi-beep](https://clawhub.ai/user/davidchyi-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill when they explicitly want an agent to forward the current or summarized conversation content to their own WeChat account for reading on a phone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send conversation content outside the chat interface to WeChat when invoked. <br>
Mitigation: Use it only after an explicit user request to send to WeChat, and confirm the destination account or message scope before sending sensitive content. <br>
Risk: The skill depends on an authenticated local wxclawbot setup and existing WeChat account credentials. <br>
Mitigation: Keep the local account configuration protected, verify wxclawbot account status before use, and prefer least-privilege local execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidchyi-beep/wechat-forward) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires wxclawbot on macOS and an existing OpenClaw WeChat account configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
