## Description:

TOTP-based OTP verification for sensitive operations such as environment variables, gateway restarts, backup deletions, and critical configuration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diegofcornejo](https://clawhub.ai/user/diegofcornejo)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to require a time-based one-time password before an agent proceeds with sensitive OpenClaw operations such as reading secrets, restarting gateways, deleting backups, or changing critical configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reusable TOTP seed can be exposed through console output, qr.png, .env files, shared terminal transcripts, or CI logs.

Mitigation: Run enrollment in a private terminal, share qr.png only through a trusted channel, delete it immediately, restrict .env access, and rotate TOTP_SECRET after any suspected exposure.

Risk: A valid OTP is a supplemental check and may not be sufficient as the only approval boundary for destructive or account-level operations.

Mitigation: Require separate review or authorization for destructive or account-level actions, and treat OTP verification as one control in a broader approval process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diegofcornejo/skills/totp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-line status strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TOTP_SECRET; setup can generate qr.png for authenticator enrollment.]

## Skill Version(s):

1.0.2 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
