## Description:

Guides developers through configuring, operating, and troubleshooting encrypted ToxTunnel TCP access to remote services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentx-icu](https://clawhub.ai/user/agentx-icu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan remote TCP access, generate scoped server and client configurations, verify deployments, and diagnose tunnel failures for services such as SSH, databases, and web apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote access rules could expose more services than intended.

Mitigation: Limit rules to exact friend keys and host:port pairs; avoid wide local binds unless protected by firewall controls.

Risk: Installing a package may start or persist a remote-access service.

Mitigation: Use version-pinned packages and review service auto-start behavior before installation.

Risk: Reloading access rules does not terminate existing connections.

Mitigation: Revoke active access at the target service or restart the tunnel server, then update rules to block new sessions.

## Reference(s):

- [ToxTunnel project homepage](https://github.com/agentx-icu/tox-tcp-tunnel)
- [ClawHub skill listing](https://clawhub.ai/agentx-icu/skills/tox-tunnel-ops)
- [Execution guidance](artifact/references/execute.md)
- [Diagnostic guidance](artifact/references/diagnose.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown with YAML configurations and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verification, troubleshooting, and rollback guidance.]

## Skill Version(s):

0.5.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
