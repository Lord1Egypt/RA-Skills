## Description:

ShieldClaw is a security suite for OpenClaw that provides security scanning, real-time protection, audit logging, and sensitive data encryption for security operations, threat detection, and data protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzming9](https://clawhub.ai/user/jzming9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use ShieldClaw to scan skills for security issues, monitor sensitive file, network, and process operations, encrypt secrets, and review audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad filesystem, network, storage, and secret-handling permissions increase the impact of incorrect or unsafe behavior.

Mitigation: Review permissions before installation, restrict sensitive paths and network access where possible, and prefer a release with narrower permissions or integrity metadata.

Risk: Advertised real-time protection and secret storage behavior is not fully auditable in the available evidence.

Mitigation: Do not rely on Guard or Vault for production protection, or store real credentials, until implementation, key handling, logging, retention, and disable controls are documented and reviewed.

## Reference(s):

- [ShieldClaw ClawHub Skill Page](https://clawhub.ai/jzming9/skills/shieldclaw)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk scores, audit summaries, security recommendations, and local configuration changes.]

## Skill Version(s):

1.0.4 (source: server release metadata, clawhub.json, CHANGELOG, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
