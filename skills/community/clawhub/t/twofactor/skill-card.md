## Description:

This skill provides guidance and enforcement rules for implementing secure two-factor authentication (2FA) using Better Auth's twoFactor plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenfengli](https://clawhub.ai/user/stevenfengli)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement Better Auth two-factor authentication flows, including TOTP, OTP delivery, backup codes, trusted devices, and 2FA session handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells users to run an unpinned third-party migration CLI that can execute changing external code and alter the auth database.

Mitigation: Review and pin the Better Auth CLI version before migration, add the reviewed version as a dev dependency, use the project lockfile, run migrations in staging first, and back up the database before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenfengli/skills/twofactor)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and TSX code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for server and client configuration, migration commands, verification flows, and security settings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
