## Description: <br>
Email API for AI agents to send email, check inboxes, read messages, extract OTP codes, search messages, and reply via ShellMail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronbatchelder](https://clawhub.ai/user/aaronbatchelder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI-agent operators use this skill to provision and operate a dedicated ShellMail inbox for automated email workflows such as unread inbox checks, OTP retrieval, message search, sending, replies, and mailbox cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent persistent access to a dedicated ShellMail inbox and OTPs through SHELLMAIL_TOKEN. <br>
Mitigation: Use a dedicated ShellMail inbox rather than personal or important email, require explicit approval before saving the token, and revoke or remove the token when access is no longer needed. <br>
Risk: The skill can send email, reply to messages, modify mail state, delete messages, and delete the address. <br>
Mitigation: Require explicit user approval before outbound, recovery, or destructive actions, and review command arguments before execution. <br>


## Reference(s): <br>
- [ShellMail homepage](https://shellmail.ai) <br>
- [ClawHub ShellMail skill page](https://clawhub.ai/aaronbatchelder/shellmail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration snippets, and ShellMail API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHELLMAIL_TOKEN and the curl and python3 binaries; ShellMail commands may read, send, modify, archive, delete, and search mailbox data.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release metadata; artifact frontmatter and skill.json report 1.2.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
