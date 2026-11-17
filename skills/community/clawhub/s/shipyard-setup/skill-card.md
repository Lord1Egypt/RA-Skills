## Description:

First-time Shipyard setup. Connects GitHub, Vercel and Supabase, stores keys safely, saves defaults. Use for "setup", "get started", "connect my accounts", "settings", or when new-app says setup is not done.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipposk](https://clawhub.ai/user/philipposk)

### License/Terms of Use:

MIT-0

## Use Case:

Beginners setting up Shipyard use this skill to connect their GitHub, Vercel, and Supabase accounts, configure optional services, and save setup defaults before building apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Supabase access token can manage all of the user's projects, and the optional Resend key has full access.

Mitigation: Keep credentials in the local keys file, never in chat, and review the full plugin before supplying credentials.

Risk: The skill's security assessment covers the supplied documentation, not the external plugin implementation.

Mitigation: Review the complete plugin and its scripts before running setup commands or providing credentials.

Risk: Setup may propose changes to global instructions.

Mitigation: Review the proposed instructions and add them only with the user's approval.

## Reference(s):

- [Accounts, step by step](references/accounts.md)
- [Troubleshooting setup](references/troubleshooting.md)
- [Install the full Shipyard plugin](https://github.com/philipposk/shipyard/blob/main/INSTALL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Resumable setup with saved progress and optional steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
