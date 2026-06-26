## Description: <br>
Guides an agent through sending WeChat messages by focusing the desktop app, using screenshots for visual context, selecting a contact, pasting text, and sending with keyboard commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noir-hedgehog](https://clawhub.ai/user/noir-hedgehog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users or operators use this skill when they want an agent to help send a WeChat message through a logged-in desktop session. It provides a checklist for finding the recipient, sending the message, and confirming the result from screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can view private WeChat screens and act through the user's logged-in account. <br>
Mitigation: Require manual confirmation of the exact recipient and message before sending, and avoid using it when private or enterprise chats are visible. <br>
Risk: The artifact includes guidance for bypassing screen-capture protections in protected apps. <br>
Mitigation: Do not use the bypass guidance for capture-protected applications, and stop the screenshot service when finished. <br>


## Reference(s): <br>
- [Wechat Sender on ClawHub](https://clawhub.ai/noir-hedgehog/wechat-sender) <br>
- [Agent-Eye](https://github.com/noir-hedgehog/Agent-eye) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes a local WeChat desktop session, peekaboo controls, and an Agent-Eye screenshot service.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
