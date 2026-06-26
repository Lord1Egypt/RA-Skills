## Description: <br>
Monitor and inspect Technitium DNS Server via its HTTP API for read-only health checks, DNS stats, zones, DHCP leases, token/session validation, and proactive alerts about DNS/DHCP issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naamah75](https://clawhub.ai/user/naamah75) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run read-only Technitium DNS Server health checks, inspect DNS and DHCP status, and summarize actionable monitoring failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Technitium API or session token, which could expose DNS administration data if over-privileged or mishandled. <br>
Mitigation: Use a dedicated read-only token, store it outside prompts and logs, and avoid administrator tokens. <br>
Risk: An incorrect or untrusted TECHNITIUM_URL could send health-check traffic and bearer tokens to the wrong endpoint. <br>
Mitigation: Verify the configured URL before use and prefer HTTPS or a trusted private network. <br>


## Reference(s): <br>
- [Technitium DNS Server](https://github.com/TechnitiumSoftware/DnsServer) <br>
- [Technitium DNS Server API docs](https://github.com/TechnitiumSoftware/DnsServer/blob/master/APIDOCS.md) <br>
- [ClawHub skill page](https://clawhub.ai/naamah75/technitium-dns) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; bundled helper emits JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TECHNITIUM_URL and TECHNITIUM_TOKEN; performs read-only Technitium HTTP API checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
