## Description:

Control a Starlink dish through its local gRPC API for status checks, WiFi client listings, speed tests, stow or unstow actions, reboots, and GPS location lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danfedick](https://clawhub.ai/user/danfedick)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate and troubleshoot a Starlink dish from an agent session while connected to the Starlink local network. It helps produce CLI-focused guidance for checking connectivity, viewing connected devices, running speed tests, stowing or unstowing the dish, rebooting it, and retrieving location data when local access is enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path uses mutable remote code from the starlink-cli repository.

Mitigation: Review and pin a specific starlink-cli revision before installation, and avoid elevated privileges during install or execution.

Risk: Stow, unstow, and reboot commands can disrupt Starlink service or physically move the dish.

Mitigation: Require explicit user confirmation before proposing or running stow, unstow, or reboot commands.

Risk: Client listing and GPS location commands can expose connected-device details or precise location data.

Mitigation: Use these commands only for explicit user requests, and minimize or redact sensitive identifiers and coordinates when sharing results.

## Reference(s):

- [starlink-cli GitHub repository](https://github.com/danfedick/starlink-cli)
- [Starlink skill on ClawHub](https://clawhub.ai/danfedick/skills/starlink)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI can produce human-readable output or JSON when commands are run with --json.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
