## Description:

Documents the MTProto protocol handling layer in Teamgram Server, including handshake, AES-IGE decryption, QuickAck, auth_key caching, and message forwarding to session service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihang9978](https://clawhub.ai/user/zhihang9978)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this reference skill to understand, debug, or extend Teamgram Server's Telegram-compatible MTProto gateway and session handling behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may blindly reuse the included Telegram-compatible app identifier constants in deployments.

Mitigation: Provision application identity and configuration for the target deployment, and treat the included constants as compatibility references rather than authorization or user-session credentials.

Risk: Reference material can become misleading if applied without checking the deployed Teamgram Server version and environment.

Mitigation: Review the referenced Teamgram Server code and service configuration before using the guidance for operational changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhihang9978/skills/teamgram-mtproto-protocol)
- [Teamgram Server repository](https://github.com/teamgram/teamgram-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown reference material with Go code snippets and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill with no executable behavior, network calls, or credential handling.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
