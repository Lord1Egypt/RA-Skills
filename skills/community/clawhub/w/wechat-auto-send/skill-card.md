## Description: <br>
Automates WeChat desktop actions to send a custom text message to a specified contact from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2450550235-debug](https://clawhub.ai/user/2450550235-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agent operators use this skill to send predefined WeChat text messages to named contacts through local desktop automation when WeChat is already installed, logged in, and visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WeChat messages from the user's logged-in account without a final confirmation. <br>
Mitigation: Require an explicit yes/no confirmation immediately before sending, and use it only for low-risk messages. <br>
Risk: Desktop focus or contact-name mismatch can send the message to the wrong window or recipient. <br>
Mitigation: Keep WeChat visible and focused, verify the recipient and message text before execution, and abort on focus errors. <br>
Risk: Sensitive content could be exposed through an unintended message send. <br>
Mitigation: Avoid passwords, keys, personal data, or other sensitive content in messages sent through this automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2450550235-debug/wechat-auto-send) <br>
- [README](artifact/README.md) <br>
- [Usage examples](artifact/EXAMPLES.md) <br>
- [OpenClaw usage notes](artifact/OPENCLAW_USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with command-line examples and execution status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local WeChat desktop session and can trigger real message sends from the logged-in account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
