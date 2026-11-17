## Description:

Guides an agent through end-to-end VLESS + Reality proxy deployment on a VPS with sing-box, Clash Verge client configuration, connectivity testing, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1126misakp](https://clawhub.ai/user/1126misakp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and maintain a self-managed VPS proxy based on VLESS, Reality, sing-box, and Clash Verge. It produces setup files, server commands, client configuration, acceptance checks, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill administers a VPS over SSH and can make persistent system changes including package installation, service creation, firewall-related tooling, fail2ban configuration, and BBR settings.

Mitigation: Use it only on VPS hosts you intend the agent to manage, review commands before execution, and keep a removal plan for the sing-box service, injected SSH key, generated secrets, and related configuration.

Risk: The workflow handles SSH credentials, generated Reality keys, upstream SOCKS credentials, and local proxy configuration files.

Mitigation: Keep credentials in local files only, avoid committing proxy-setup-info.txt or .proxy-keys.txt, and rotate or remove credentials after use when they are no longer needed.

Risk: The skill downloads sing-box release artifacts dynamically and installs them on the target server.

Mitigation: Pin and verify downloaded binaries before installation when using the skill in a sensitive environment.

Risk: The generated proxy can be used in regulated network environments or locations with legal restrictions.

Mitigation: Use the skill only for lawful, authorized network access and confirm the applicable regional rules before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1126misakp/skills/proxy-expert)
- [sing-box documentation](https://sing-box.sagernet.org)
- [Clash Verge Rev install page](https://clashvergerev.com/install)
- [Server configuration templates](references/server-configs.md)
- [Client configuration template](references/client-config.md)
- [Troubleshooting guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, YAML configuration, and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce proxy-setup-info.txt, .proxy-keys.txt, clash-verge-config.yaml, and proxy-acceptance-report.md during use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
