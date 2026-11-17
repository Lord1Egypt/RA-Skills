## Description:

Configures and checks ZeroTier-based remote web access for OpenClaw by updating gateway binding, allowed origins, and gateway restart steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maoyf0571](https://clawhub.ai/user/maoyf0571)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect ZeroTier and OpenClaw gateway status, enable remote access to the OpenClaw web control UI, and restore local-only access when remote access is no longer needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose the OpenClaw gateway more broadly than its ZeroTier-only purpose by binding the gateway to 0.0.0.0.

Mitigation: Bind only to a trusted ZeroTier address or interface and restrict firewall rules to the ZeroTier interface or subnet.

Risk: The artifact weakens authentication controls by enabling insecure authentication and disabling device authentication in the gateway configuration example.

Mitigation: Keep device authentication enabled, avoid insecure authentication settings, and review the generated gateway configuration before restarting the service.

Risk: The enable flow prints or preserves an access token that could appear in terminal logs or backups.

Mitigation: Treat the token as secret material and rotate it if it appears in logs, screenshots, shared terminals, or backups.

Risk: The prerequisite documentation suggests a pipe-to-sudo ZeroTier installer.

Mitigation: Install ZeroTier through a trusted package-management path or review the installer before running privileged commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maoyf0571/skills/zerotier-remote-web)
- [ZeroTier](https://zerotier.com)
- [ZeroTier Documentation](https://zerotier.atlassian.net/wiki/)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local command execution that changes OpenClaw gateway configuration and restarts the gateway service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
