## Description:

Create and manage RizzForms-backed web forms, webhook delivery, submissions, and embed HTML using the RizzForms API guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blairanderson](https://clawhub.ai/user/blairanderson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to add contact, feedback, signup, lead capture, waitlist, or other web forms backed by RizzForms. It helps configure webhook delivery, inspect submissions, handle spam-related behavior, and generate embeddable HTML or JSON submission examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use broad RizzForms authority over forms, webhooks, and submissions.

Mitigation: Use the narrowest API key permissions available and require confirmation before creating or changing forms, webhooks, or submission access.

Risk: Form submissions and webhook payloads may contain personal data.

Mitigation: Minimize collected fields, limit exposure of payloads, and handle submissions according to applicable privacy obligations.

Risk: The artifact claims a bundled CLI, but the inspected artifact does not include that CLI.

Mitigation: Verify available tooling before following CLI-specific steps; when the CLI is absent, rely on the documented API workflow instead.

## Reference(s):

- [RizzForms API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline HTML, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API calls, form embed snippets, webhook configuration guidance, and submission-management steps that require a RizzForms API key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
