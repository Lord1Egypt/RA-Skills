## Description:

Use when capturing outbound email in development or staging without delivering to real recipients, inspecting HTML or headers, running spam or structure checks, or automating tests against a fake inbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailtrap](https://clawhub.ai/user/mailtrap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to route development, staging, CI, or demo email into Mailtrap Email Sandbox for inspection and automated checks without delivering to real recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sandbox and production credentials or endpoints may be confused, causing failed delivery expectations or token misuse.

Mitigation: Keep sandbox tokens separate from production tokens and confirm that sandbox endpoints and credentials are used only in development, staging, CI, or demos.

Risk: Test messages may include real customer data when routed into a sandbox.

Mitigation: Avoid placing real customer data in test messages unless the team's data handling policy permits it.

Risk: Generated SDK examples may become stale as Mailtrap SDK options change.

Mitigation: Confirm SDK-specific sandbox mode options against the official linked documentation before generating or applying code.

## Reference(s):

- [Mailtrap Developer Documentation](https://docs.mailtrap.io/developers/)
- [Sandboxes API](https://docs.mailtrap.io/developers/email-sandbox/sandboxes-inboxes.md)
- [Email Sandbox Messages](https://docs.mailtrap.io/developers/email-sandbox/messages.md)
- [Send Test Emails](https://docs.mailtrap.io/developers/email-sandbox/send-test-emails.md)
- [Handlebars Templates](https://docs.mailtrap.io/email-api-smtp/email-templates/handlebars.md)
- [Mailtrap Node.js SDK](https://github.com/mailtrap/mailtrap-nodejs)
- [Mailtrap Python SDK](https://github.com/mailtrap/mailtrap-python)
- [Mailtrap PHP SDK](https://github.com/mailtrap/mailtrap-php)
- [Mailtrap Ruby SDK](https://github.com/mailtrap/mailtrap-ruby)
- [Mailtrap Java SDK](https://github.com/mailtrap/mailtrap-java)
- [Mailtrap .NET SDK](https://github.com/mailtrap/mailtrap-dotnet)
- [Mailtrap CLI](https://github.com/mailtrap/mailtrap-cli)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with endpoint references, configuration values, and code or command examples when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable skill code; generated advice should be checked against current Mailtrap SDK documentation before implementation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
