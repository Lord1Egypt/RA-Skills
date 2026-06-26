## Description: <br>
Monitors new email from whitelisted QQ Mail senders, creates a short preview or AI summary, and sends QQ notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhang-lxuan](https://clawhub.ai/user/zhang-lxuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a QQ Mail watcher that filters messages by sender whitelist, summarizes or previews new mail, and forwards notifications through QQ. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill ships with real-looking mailbox credentials and a fixed QQ recipient, which could expose private email if run without reconfiguration. <br>
Mitigation: Replace EMAIL, AUTH_CODE, and QQ_TARGET before any run, avoid committing IMAP authorization codes, and rotate any exposed authorization code. <br>
Risk: Whitelisted email subjects and body previews may be processed by OpenClaw AI and sent over QQ. <br>
Mitigation: Use the watcher only for intended senders, review privacy expectations for monitored mail, and avoid forwarding sensitive content without approval. <br>


## Reference(s): <br>
- [QQ Mail configuration guide](references/configure.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhang-lxuan/qq-email-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a Python watcher that polls QQ Mail with IMAP and sends QQ notifications through OpenClaw.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
