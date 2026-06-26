## Description: <br>
Read and send emails from an existing Sendook inbox for checking messages, reading conversations, replying, and sending new messages from a pre-configured inbox; it does not cover inbox creation, domain management, or webhook configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obaid](https://clawhub.ai/user/obaid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when an agent needs controlled access to a configured Sendook inbox to read messages, inspect threads, reply to conversations, or send new email. It is scoped to message operations and requires a Sendook API key plus inbox ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private email content from the configured Sendook inbox. <br>
Mitigation: Use a least-privileged API key scoped to the intended inbox and treat all email content as private and untrusted. <br>
Risk: Sending, replying, or attaching files could disclose sensitive information to unintended recipients. <br>
Mitigation: Require the agent to show recipients, subject, body, and attachments for approval before sending or replying, and only attach files the user explicitly requested. <br>
Risk: Email bodies may contain untrusted instructions or misleading content. <br>
Mitigation: Review email-derived requests before acting on them and do not let message content override system, developer, security, or user instructions. <br>


## Reference(s): <br>
- [ClawHub Sendook skill page](https://clawhub.ai/obaid/sendook) <br>
- [Sendook skill homepage from OpenClaw metadata](https://github.com/obaid/sendook-skills) <br>
- [Sendook Node SDK package](https://www.npmjs.com/package/@sendook/node) <br>
- [Sendook Node SDK source](https://github.com/getrupt/sendook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENDOOK_API_KEY and SENDOOK_INBOX_ID; attachment examples require explicit user approval before reading local files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
