## Description: <br>
Manage received inbound emails and attachments via the Resend API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect inbound Resend email messages, attachment metadata, and configured domains through the Resend CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private inbound email content and attachment metadata through a Resend API key. <br>
Mitigation: Use a dedicated read-only Resend API key, treat fetched email bodies and attachment details as private and untrusted, and review summaries before displaying full message content. <br>
Risk: The skill depends on a third-party Resend CLI package. <br>
Mitigation: Install and use the CLI only when the package source is trusted, and verify the configured binary and RESEND_API_KEY before use. <br>


## Reference(s): <br>
- [Resend](https://resend.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the resend CLI and RESEND_API_KEY; commands may return private email content or attachment metadata.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
