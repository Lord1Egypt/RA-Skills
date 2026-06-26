## Description: <br>
Manage Tailscale tailnet via CLI and API for status checks, device management, file transfer, service exposure, SSH, auth keys, DNS, and ACL tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmagar](https://clawhub.ai/user/jmagar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, administrators, and operators use this skill to inspect and manage a Tailscale tailnet through local CLI commands and tailnet-wide API operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help administer a Tailscale tailnet, including actions that expose services, remove devices, change MagicDNS or ACL access, or create auth keys. <br>
Mitigation: Review commands before running them and use extra care with Funnel, device deletion, MagicDNS changes, ACL changes, and auth key creation. <br>
Risk: Tailnet-wide API operations require a Tailscale API key. <br>
Mitigation: Keep the API key protected, scope it narrowly, and store it only in the documented credentials file or environment variable. <br>


## Reference(s): <br>
- [Tailscale Admin Console API Keys](https://login.tailscale.com/admin/settings/keys) <br>
- [Tailscale Download](https://tailscale.com/download) <br>
- [ClawHub Tailscale Skill Page](https://clawhub.ai/jmagar/tailscale) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON output from Tailscale CLI or API helper commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
