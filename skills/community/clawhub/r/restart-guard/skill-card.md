## Description:

Deterministic OpenClaw gateway restart with down/up state-machine verification, origin-session proactive ACK, and backward-compatible config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjianru](https://clawhub.ai/user/zjianru)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Restart Guard to restart an OpenClaw gateway while preserving context, verifying the down/up recovery sequence, and delivering a post-restart report to the originating session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can restart OpenClaw gateway infrastructure.

Mitigation: Use it only in a controlled OpenClaw environment and require explicit operator confirmation before restart.

Risk: Configured diagnostics or verification commands could be overly broad.

Mitigation: Restrict diagnostics and verification commands to known OpenClaw commands; the artifact documents strict non-shell execution and rejection of shell metacharacters.

Risk: Gateway credentials, notification tokens, or restart context files could be exposed if storage or endpoint scope is weak.

Mitigation: Keep the gateway host loopback-only unless the endpoint is fully trusted, avoid arbitrary auth_token_env values, and protect ~/.openclaw/.env plus restart context files with strict permissions.

## Reference(s):

- [README](artifact/README.md)
- [Enhanced Restart Implementation Spec](artifact/ENHANCED_RESTART_IMPLEMENTATION_SPEC.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell commands with generated restart context and diagnostic files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces restart status events, concise user-facing reports, local diagnostics, and notification routing metadata.]

## Skill Version(s):

2.2.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
