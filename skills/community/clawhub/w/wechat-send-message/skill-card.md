## Description: <br>
在微信 Mac 版发送消息，适用于用户提到"微信发消息"、"发微信"或"给 XXX 发微信"的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvin-dean](https://clawhub.ai/user/calvin-dean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who automate messaging on macOS use this skill to search for a WeChat contact and send a message through the WeChat Mac interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send a real WeChat message from the user's account without confirming the exact recipient or message first. <br>
Mitigation: Preview the recipient and message, handle ambiguous contact matches, and require explicit approval before pressing Enter to send. <br>
Risk: The skill controls the Mac WeChat UI, so unintended focus or contact selection could affect the message target. <br>
Mitigation: Run only when the WeChat window state is visible and expected, and verify the selected conversation before entering message content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvin-dean/wechat-send-message) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell and AppleScript command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces UI automation steps that can send messages from the user's WeChat account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
