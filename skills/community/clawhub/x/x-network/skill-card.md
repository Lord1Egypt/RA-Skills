## Description: <br>
This skill provides comprehensive network administration and diagnostic tools through x-cmd CLI, including network scanning with Nmap, ARP table management, DNS configuration, routing table analysis, and enhanced ping utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tzw-my](https://clawhub.ai/user/tzw-my) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network administrators, security professionals, and system administrators use this skill to generate command-line guidance for diagnosing connectivity, mapping networks, inspecting ARP and routing data, managing DNS settings, and monitoring latency or service availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network scans can affect systems outside the user's authority or trigger operational and legal issues. <br>
Mitigation: Run scanning commands only on networks the user owns or is authorized to test, and avoid broad or stealth scans unless explicitly approved. <br>
Risk: DNS-setting commands can change system-wide name resolution and may require administrator privileges. <br>
Mitigation: Review DNS changes carefully before execution, confirm the intended resolver settings, and use appropriate privileges only when needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/tzw-my/x-network) <br>
- [x-cmd Network Documentation](https://x-cmd.com/mod/network) <br>
- [Nmap Official Documentation](https://nmap.org/docs.html) <br>
- [x-cmd ARP Management](https://x-cmd.com/mod/arp) <br>
- [x-cmd DNS Configuration](https://x-cmd.com/mod/dns) <br>
- [x-cmd Enhanced Ping](https://x-cmd.com/mod/ping) <br>
- [x-cmd TCP Ping](https://x-cmd.com/mod/tping) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that require network access, installed x-cmd or Nmap tooling, and elevated privileges for some scan or DNS operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
