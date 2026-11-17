## Description:

Provides OpenClaw session passphrase authentication with password hashing, recovery options, lockout protection, audit logging, and paid billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squallsol](https://clawhub.ai/user/squallsol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add a passphrase gate to OpenClaw sessions, including setup, timeout handling, account recovery, and uninstall workflows. It is also used to enforce the skill's paid per-call billing flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security verdict is suspicious for a session-password guard that handles session access, recovery secrets, local audit/state files, and paid billing calls.

Mitigation: Review carefully before installing and do not rely on it as a security boundary until the authentication schema, recovery flow, billing consent, and credential-handling issues identified by evidence.security are fixed.

Risk: The artifact includes paid billing behavior and evidence.security flags consent and hardcoded credential concerns.

Mitigation: Require explicit user billing consent before charges, move billing credentials out of bundled source, and rotate any exposed payment API key before use.

Risk: Recovery and local state handling involve sensitive secrets and files, and the artifact includes recovery stub behavior that can expose recovery codes during setup or testing.

Mitigation: Use a real configured mail transport, disable stub recovery output in production, restrict local file permissions, and clear recovery artifacts after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/squallsol/skills/session-password)
- [Feature Specification](docs/FEATURE_SPEC.md)
- [User Manual](docs/USER_MANUAL.md)
- [SkillPay Payment Page](https://skillpay.me/skill/6387f3fa-cceb-4a60-afd4-fc1f4eb2d7c3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands, JSON status output, and local configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bilingual English and Chinese user-facing messages; stores authentication state, audit logs, recovery records, and configuration under the OpenClaw workspace memory directory.]

## Skill Version(s):

1.6.1 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
