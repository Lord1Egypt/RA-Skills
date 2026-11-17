## Description:

Read, search, and manage Zoho Mail via the Zoho Mail REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ragsagar](https://clawhub.ai/user/ragsagar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure Zoho OAuth credentials and have an agent read, search, inspect, and summarize Zoho Mail data through documented REST API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and search mail for the configured Zoho account when OAuth credentials are provided.

Mitigation: Install only for intended accounts and use the listed read-only OAuth scopes.

Risk: Zoho client secrets and refresh tokens can expose mailbox access if shared through shells, logs, tickets, or chat.

Mitigation: Keep credentials out of shared contexts and revoke the refresh token in Zoho if it is exposed or no longer needed.

Risk: Using the wrong regional Zoho endpoint can cause authentication or mail API calls to fail.

Mitigation: Use the mail and auth endpoints that match the Zoho account region.

## Reference(s):

- [Zoho Mail API Documentation](https://www.zoho.com/mail/help/api/)
- [Zoho API Console](https://api-console.zoho.com/)
- [ClawHub Skill Page](https://clawhub.ai/ragsagar/skills/zoho-mail-skill)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and Zoho OAuth environment variables for the configured account.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
