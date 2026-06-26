## Description: <br>
Pushbullet provides an OAuth-backed integration for sending pushes, sharing links and files, managing devices, creating chats, and handling cross-device messaging through ClawLink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to automate Pushbullet notifications, file and link sharing, push history review, device management, and chat management from an agent workflow. It is intended for explicit Pushbullet tasks after the user has connected a Pushbullet account through ClawLink OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Pushbullet OAuth connection and sensitive account access through ClawLink. <br>
Mitigation: Install it only when the user trusts ClawLink with the Pushbullet connection and use it only for explicit Pushbullet tasks. <br>
Risk: Write and destructive operations can create, update, delete, or clear Pushbullet pushes, chats, and devices. <br>
Mitigation: Review send, update, delete, and clear-all requests carefully before execution. <br>
Risk: File pushes, links, notes, chat data, device identifiers, and push history may leave or be exposed through the connected Pushbullet account and related upload infrastructure. <br>
Mitigation: Avoid sharing sensitive content unless the user intends it to pass through Pushbullet and any required upload flow. <br>


## Reference(s): <br>
- [Pushbullet API Docs](https://docs.pushbullet.com) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Pushbullet Skill Page](https://clawhub.ai/hith3sh/pushbullet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Pushbullet OAuth account through ClawLink; write and destructive actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
