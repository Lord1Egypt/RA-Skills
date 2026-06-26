## Description: <br>
QQ邮箱接收与发送skill - 读取QQ邮箱中的邮件和发送邮件到其他账号 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cynic-Joe](https://clawhub.ai/user/Cynic-Joe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users configure an agent to read recent QQ Mail inbox messages and send messages through QQ Mail using local IMAP and SMTP credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for mailbox authorization credentials and may store them in a local .env file. <br>
Mitigation: Use QQ Mail authorization codes rather than account passwords, store the .env file locally with restricted access, and revoke or rotate credentials after use. <br>
Risk: The skill can read mailbox contents and send email from the configured account. <br>
Mitigation: Install only when mailbox read/send access is intended, review messages and recipients before sending, and avoid using high-privilege or shared mailboxes. <br>
Risk: Dependency versions are not pinned to exact patched releases. <br>
Mitigation: Review and lock dependency versions in the deployment environment before production use. <br>


## Reference(s): <br>
- [QQ Mail](https://mail.qq.com) <br>
- [ClawHub skill page](https://clawhub.ai/Cynic-Joe/qqemail-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update a local .env configuration file when the user consents to credential setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
