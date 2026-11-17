## Description:

Share code snippets and files securely via snipit.sh with AES-256 encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[homecity](https://clawhub.ai/user/homecity)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to share code, configuration snippets, logs, diffs, and build output through snipit.sh using the snipit CLI or curl API fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send code, logs, configuration, .env files, or secrets to an external sharing service.

Mitigation: Use it only for material approved for snipit.sh, redact secrets and personal data first, and prefer approved internal sharing or secret-management tools for credentials.

Risk: The documented password option can expose real passwords through command history or process inspection when passed directly on the command line.

Mitigation: Do not pass real passwords directly on the command line; use safer secret-handling practices or approved internal tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/homecity/skills/snipit)
- [snipit.sh create snippet API](https://snipit.sh/api/snippets)
- [snipit.sh retrieve snippet API](https://snipit.sh/api/snippets/{id})

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include snipit CLI commands, curl API examples, and sharing options such as password protection, burn-after-read, and expiration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
