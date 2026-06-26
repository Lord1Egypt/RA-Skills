## Description: <br>
Guides agents through using Telethon QR login as a workaround for Telegram PHONE_CODE_EXPIRED login failures, including setup commands, a Python example, and troubleshooting notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polityang](https://clawhub.ai/user/polityang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill when Telegram phone-code login fails on a new device and they need QR-based Telethon login guidance. It also helps them understand session reuse, common Telegram login errors, and safe handling of generated QR images and session files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles Telegram API credentials, QR login images, and session files that can grant account access. <br>
Mitigation: Use the steps only on a trusted machine, keep credentials, QR images, and session files secret, and revoke Telegram sessions that are no longer needed. <br>
Risk: The artifact includes publishing steps involving GitHub PATs and ClawHub tokens, which are sensitive credentials. <br>
Mitigation: Perform publishing through your own authenticated browser or CLI session, do not share PATs or login QR images with another person or agent, and revoke tokens that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/polityang/telegram-qr-login-workaround) <br>
- [Telegram API portal](https://my.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential-sensitive login guidance involving Telegram API credentials, QR images, and session files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
