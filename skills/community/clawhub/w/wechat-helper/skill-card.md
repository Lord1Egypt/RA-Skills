## Description: <br>
Automates a browser session for WeChat File Helper to send text messages and handle login QR code capture through configured messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qidu](https://clawhub.ai/user/qidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to automate short WeChat File Helper messages from a browser session, including QR-code login handling when the session is logged out. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Login QR screenshots can be sent through configured messaging channels without strong recipient checks. <br>
Mitigation: Use an explicit trusted recipient, avoid empty or default recipients, and require confirmation before sending QR screenshots. <br>
Risk: Cron or monitor execution can send WeChat messages or QR media automatically. <br>
Mitigation: Enable cron only in controlled environments, review the configured message channels, and keep browser/session automation under operator supervision. <br>
Risk: Captured QR images may remain at /tmp/wechat-qr.png after use. <br>
Mitigation: Delete the QR screenshot after delivery or adjust the scripts to clean it up automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qidu/wechat-helper) <br>
- [WeChat File Helper web app](https://filehelper.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with browser and messaging command examples plus shell script usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a QR screenshot at /tmp/wechat-qr.png and send media messages through configured channels when scripts are executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
