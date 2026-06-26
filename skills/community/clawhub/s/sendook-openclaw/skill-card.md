## Description: <br>
Read and send emails from an existing Sendook inbox, including listing messages, reading threads, sending messages, and replying from a pre-configured inbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obaid](https://clawhub.ai/user/obaid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with email in a configured Sendook inbox. It is intended for message workflows only, such as checking new mail, reading conversations, sending new messages, and replying to existing threads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured credentials allow the agent to read and send email from the selected Sendook inbox. <br>
Mitigation: Use a least-privileged SENDOOK_API_KEY and restrict SENDOOK_INBOX_ID to the intended inbox. <br>
Risk: The agent could send an incorrect or unintended outbound email. <br>
Mitigation: Review important outbound emails and replies before sending. <br>
Risk: Attachments can expose local files if selected carelessly. <br>
Mitigation: Only allow attachments that were explicitly selected and avoid credential files or files outside the intended project scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/obaid/sendook-openclaw) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/obaid) <br>
- [Skill homepage](https://github.com/obaid/sendook-skills) <br>
- [Sendook Node SDK package](https://www.npmjs.com/package/@sendook/node) <br>
- [Sendook Node SDK source](https://github.com/getrupt/sendook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, shell, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENDOOK_API_KEY and SENDOOK_INBOX_ID; operations are scoped to an existing configured inbox.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
