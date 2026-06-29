## Description: <br>
Expose local SSH servers to the public internet via aitun TCP tunnel with SSH-over-TLS routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctz168](https://clawhub.ai/user/ctz168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to publish temporary SSH access for machines behind NAT, firewalls, containers, or private networks. It is intended for remote debugging, maintenance, pair programming, and agent access workflows that need SSH-over-TLS routing through aitun. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a local SSH server through a public tunnel, which can publish a powerful administrative service beyond the local network. <br>
Mitigation: Use it only for machines intentionally exposed for SSH access, keep tunnels temporary, require key-only SSH with strong access controls, and stop the tunnel when finished. <br>
Risk: The artifact includes remote script installer examples and a Python TLS example that disables certificate verification. <br>
Mitigation: Prefer pip or uv installation paths, review installer scripts before execution, and avoid disabling TLS verification in production SSH automation. <br>
Risk: The security verdict is suspicious because the safety controls are under-scoped for a remote SSH exposure workflow. <br>
Mitigation: Review carefully before installing, limit exposed accounts and ports, monitor SSH access, and undo SSH or remote-login service changes after use. <br>


## Reference(s): <br>
- [AiTun homepage](https://aitun.cc) <br>
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/sshtunnel) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ctz168) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, PowerShell, SSH config, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides install, tunnel setup, SSH client configuration, connection reuse, cleanup, and security guidance.] <br>

## Skill Version(s): <br>
4.7.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
