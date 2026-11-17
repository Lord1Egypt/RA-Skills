## Description:

This skill provides comprehensive network administration and diagnostic tools through x-cmd CLI, including network scanning with Nmap, ARP table management, DNS configuration, routing table analysis, and enhanced ping utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tzw-my](https://clawhub.ai/user/tzw-my)

### License/Terms of Use:

MIT-0

## Use Case:

Network administrators, security professionals, system administrators, and developers use this skill to generate x-cmd based guidance and commands for network diagnostics, connectivity troubleshooting, network discovery, DNS inspection, route analysis, and performance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Active network scans can probe systems outside the user's authorization.

Mitigation: Run scans only against systems the user owns or has explicit permission to test, and review targets before executing commands.

Risk: DNS setting changes can disrupt connectivity or redirect traffic.

Mitigation: Review DNS commands before execution, confirm administrative intent, and preserve current DNS settings before making changes.

Risk: Some scan types and network configuration actions may require elevated privileges.

Mitigation: Use the least privilege needed and avoid privileged commands unless the user understands the operational impact.

## Reference(s):

- [x-cmd Network Documentation](https://x-cmd.com/mod/network)
- [Nmap Official Documentation](https://nmap.org/docs.html)
- [x-cmd ARP Management](https://x-cmd.com/mod/arp)
- [x-cmd DNS Configuration](https://x-cmd.com/mod/dns)
- [x-cmd Enhanced Ping](https://x-cmd.com/mod/ping)
- [x-cmd TCP Ping](https://x-cmd.com/mod/tping)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples for network probing, diagnostics, visualization, and DNS or route inspection.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
