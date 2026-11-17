## Description:

Resend Skills helps agents work with the Resend email API for transactional email, inbound webhooks, templates, delivery events, domains, contacts, broadcasts, API keys, automations, logs, and SDK setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christina-de-martinez](https://clawhub.ai/user/christina-de-martinez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to get implementation guidance, examples, and operational cautions for building email workflows with Resend. It covers sending and receiving email, managing Resend account resources, choosing SDKs, and avoiding common production issues such as duplicate sends, unverified webhooks, and exposed secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real email sends, account changes, deletion operations, and webhook updates can affect production Resend resources.

Mitigation: Use least-privilege Resend API keys and confirm send, delete, API-key, and webhook actions before running them.

Risk: Resend API keys, webhook secrets, logs, and attachments may contain sensitive data.

Mitigation: Store secrets in environment variables, avoid logging complete secrets, and treat logs and attachments as sensitive.

Risk: Unpinned SDK or external skill dependencies can reduce reproducibility.

Mitigation: Pin SDK or external skill dependencies when the deployment environment requires reproducible installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/christina-de-martinez/skills/resend-skills)
- [Resend skill documentation](https://resend.com/docs/resend-skill)
- [Resend agent skills](https://resend.com/agent-skills)
- [Resend API reference](https://resend.com/docs/api-reference)
- [Resend documentation](https://resend.com/docs)
- [Resend skills repository](https://github.com/resend/resend-skills)
- [Sending overview](references/sending/overview.md)
- [Sending best practices](references/sending/best-practices.md)
- [Receiving](references/receiving.md)
- [Webhooks](references/webhooks.md)
- [Templates](references/templates.md)
- [Domains](references/domains.md)
- [Installation](references/installation.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code examples, API usage notes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Resend API calls, SDK installation commands, environment variable guidance, and operational warnings.]

## Skill Version(s):

3.3.3 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
