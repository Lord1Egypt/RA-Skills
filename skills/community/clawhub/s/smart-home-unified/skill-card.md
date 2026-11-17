## Description:

Provides ClawHub agent guidance and Node.js CLI scaffolding for configuring and controlling smart-home devices, with evidence of Xiaomi Mi Home and Apple HomeKit integration paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External smart-home users and agent operators use this skill to configure smart-home credentials, list or control supported devices, and draft automation workflows from one agent-accessible interface. Reviewers should confirm supported platforms and commands before relying on the advertised broader automation claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to place Xiaomi, Apple, HomeKit, or device credentials in TOOLS.md, which can expose high-value smart-home secrets if the file is shared or committed.

Mitigation: Use a secret manager or environment variables instead of plaintext TOOLS.md entries, restrict local file permissions, and rotate any tokens or passwords that were stored in plaintext.

Risk: The security evidence flags unsupported security and capability claims, and artifact behavior shows several advertised commands or platforms are still scaffolded or simplified.

Mitigation: Treat the release as a prototype, verify exact supported devices and actions in a test environment, and avoid paid or production reliance until the publisher documents implemented features and privacy practices.

Risk: Running smart-home control code can affect physical devices and local-network access.

Mitigation: Review the code and dependency versions before connecting real devices, start with noncritical devices on a trusted local network, and limit account permissions where the platform allows it.

## Reference(s):

- [Smart Home Unified ClawHub listing](https://clawhub.ai/lvjunjie-byte/skills/smart-home-unified)
- [lvjunjie-byte ClawHub publisher profile](https://clawhub.ai/user/lvjunjie-byte)
- [miio library documentation](https://github.com/aholstenson/miio)
- [HAP-NodeJS documentation](https://github.com/homebridge/HAP-NodeJS)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include device-control commands and credential setup examples that require user-supplied smart-home account or device secrets.]

## Skill Version(s):

1.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
