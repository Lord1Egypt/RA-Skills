## Description: <br>
客服邮件智能分流：用 CLI 关键词预筛自动回复常见问题，并将复杂邮件转发到 AI 处理邮箱或人工邮箱。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devincodel](https://clawhub.ai/user/devincodel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and independent SaaS operators use this skill to set up automated support email triage. It auto-replies to pricing and cancellation FAQs, forwards business mail to a human mailbox, and sends bug or unclassified mail to an AI analysis mailbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the release suspicious because the automated mail script builds shell commands from incoming email data while handling customer messages. <br>
Mitigation: Review before installing on a real support mailbox; replace shell-string command execution with argument-array execution such as spawn or execFile, or apply strict validation and escaping for sender addresses, message IDs, profiles, and folder IDs. <br>
Risk: Forwarding full customer emails to the csbot and human mailbox may expose support data beyond the original support inbox. <br>
Mitigation: Confirm that the forwarding flow matches the product privacy notice and support-data handling requirements before using it with real customer messages. <br>
Risk: A support mailbox channel installation or vague scheduled task can bypass the router and cause duplicate or unintended handling. <br>
Mitigation: Use a separate support inbox and csbot inbox, install the channel only for csbot, schedule the explicit node router command in an isolated session, and set delivery to none. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/devincodel/support-router) <br>
- [Publisher profile](https://clawhub.ai/user/devincodel) <br>
- [mail-cli package](https://www.npmjs.com/package/@clawemail/mail-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration, shell commands, and JavaScript router behavior; the router can emit JSON status for tests and polling results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, mail-cli, configured support and csbot mail profiles, and a scheduled polling job.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
