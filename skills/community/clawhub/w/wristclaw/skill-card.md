## Description:

Bridges the WristClaw watch and OpenClaw agent by recognizing pairing payloads, registering the native WristClaw channel after explicit confirmation, and keeping replies concise for the watch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salam](https://clawhub.ai/user/salam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use WristClaw to pair an Apple Watch with an OpenClaw agent so watch-originated requests can be answered through a concise encrypted channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paired watch receives ongoing broad access to the OpenClaw agent.

Mitigation: Install only when that access is acceptable, require explicit pairing confirmation, and revoke the channel with the documented remove command when no longer needed.

Risk: The release installs a high-impact external plugin through mutable or unpinned paths.

Mitigation: Prefer an exact audited package version, verify the package or release hash before global installation, and inspect the shell installer before running it.

Risk: Custom relay URLs can change the trust boundary for session routing.

Mitigation: Use the default allowlisted relay unless the user explicitly approves a custom relay.

## Reference(s):

- [WristClaw ClawHub listing](https://clawhub.ai/salam/skills/wristclaw)
- [WristClaw homepage](https://wristclaw.app)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text guidance with shell commands and channel configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Watch-facing replies are expected to be concise plain text; the channel may carry text, audio, and small images.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
