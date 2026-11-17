## Description:

Use when working with QJZD Nav CLI login, bearer token auth, profile setup, profile switching, current profile inspection, or fixing missing keyring credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nqdy666](https://clawhub.ai/user/nqdy666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and inspect QJZD Nav CLI authentication, bearer token access, profiles, and keyring-backed credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Password login examples can lead users to put real passwords directly in shell commands.

Mitigation: Prefer interactive login or a secret manager based path when available, and avoid placing real passwords in shell history or shared automation logs.

Risk: Forced profile deletion can remove saved access material for the wrong or production profile.

Mitigation: Confirm the exact profile name and impact before using forced deletion, especially for production profiles.

## Reference(s):

- [Qjzd Nav Cli Auth on ClawHub](https://clawhub.ai/nqdy666/skills/qjzd-nav-cli-auth)
- [QJZD Nav service endpoint](https://nav.qjzd.online)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-mode command guidance when another tool needs structured CLI output.]

## Skill Version(s):

1.3.2 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
