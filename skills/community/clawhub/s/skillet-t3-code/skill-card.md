## Description:

Use when configuring or troubleshooting T3 Code projects, multi-machine environments, desktop or headless servers, project names or icons, updates, launchers, or private remote access. Trigger on stale project entries, wrong workspace identity, missing favicons, update banners, saved backend setup, server reachability, Tailscale exposure, SSH tunnel fallback, or T3 service setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to configure and troubleshoot T3 Code projects, desktop and headless servers, project state, updates, and private access across multiple machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended server examples can run newly published software without a separate update decision.

Mitigation: Pin the service to a specific reviewed T3 release, approve updates separately, retain a working version for rollback, and confirm who can access each remote server.

## Reference(s):

- [T3 Code skill page](https://clawhub.ai/escoffier-labs/skills/skillet-t3-code)
- [T3 Code official website](https://t3.codes)
- [T3 Code downloads](https://t3.codes/download)
- [T3 Code project repository](https://github.com/pingdotgg/t3code)
- [T3 Code releases](https://github.com/pingdotgg/t3code/releases)
- [T3 CLI package](https://www.npmjs.com/package/t3)
- [Multi-Machine T3 Code Setup](artifact/references/multi-machine.md)
- [Project State and Icons](artifact/references/project-state.md)
- [T3 Code over Tailscale](artifact/references/remote-tailscale.md)
- [Updates, Launchers, and Local Automation](artifact/references/updates-and-launchers.md)
- [Windows Remote Host](artifact/references/windows-remote.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Procedural Markdown with shell and PowerShell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on the installed T3 version, operating system, and network setup.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata; bundled skill frontmatter reports 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
