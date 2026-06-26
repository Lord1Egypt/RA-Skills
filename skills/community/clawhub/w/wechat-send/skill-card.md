## Description: <br>
Automates sending text messages in the macOS WeChat desktop app by controlling the visible GUI with AppleScript and JXA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clk1st](https://clawhub.ai/user/clk1st) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to send text-only WeChat messages to exact contacts from a logged-in macOS WeChat desktop session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted contact or message text could alter the AppleScript automation. <br>
Mitigation: Use exact recipient names and trusted message text; prefer a revised version that safely escapes AppleScript input before execution. <br>
Risk: The skill sends real WeChat messages without a confirmation step. <br>
Mitigation: Confirm the recipient and message content before invoking the script, especially for batch messaging. <br>
Risk: Contact search selects the first result, which can send a message to the wrong person if names are ambiguous. <br>
Mitigation: Use specific contact names and verify the WeChat window state before sending. <br>
Risk: The script sets the macOS clipboard to the outgoing message. <br>
Mitigation: Prefer a revised version that preserves and restores clipboard contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clk1st/wechat-send) <br>
- [Publisher profile](https://clawhub.ai/user/clk1st) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [wechat_send.sh](artifact/scripts/wechat_send.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Shell command invocation with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a contact name and message text; sends one text message per invocation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
