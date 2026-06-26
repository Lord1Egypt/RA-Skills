## Description: <br>
TunnelProxy lets an AI agent connect to a user-run local TunnelProxy service to execute shell commands, transfer files, and route HTTP requests through the user's machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turinfohlen](https://clawhub.ai/user/turinfohlen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a cloud agent needs capabilities available on a trusted local machine, such as shell execution, local file transfer, or access through the user's network. It is only appropriate for fully trusted agents because the skill grants broad control over the user's computer and network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A connected agent can execute commands and access files with the permissions of the TunnelProxy process. <br>
Mitigation: Run the service in an isolated VM or a dedicated low-privilege account and review commands before granting access. <br>
Risk: Exposing the service publicly can allow agent traffic to use the user's network and reach sensitive internal resources. <br>
Mitigation: Bind to localhost unless public access is explicitly required, avoid workplace or internal networks without authorization, and use firewall rules for additional isolation. <br>
Risk: Long-lived or weak access tokens can preserve high-impact access after the intended task ends. <br>
Mitigation: Use strong short-lived tokens, rotate secrets after use, and inspect TunnelProxy access logs for unexpected activity. <br>


## Reference(s): <br>
- [TunnelProxy ClawHub Page](https://clawhub.ai/turinfohlen/tunnel-proxy) <br>
- [TunnelProxy source repository](https://github.com/TurinFohlen/tunnel_proxy) <br>
- [Protocol Reference](references/protocol.md) <br>
- [README for Users](references/README_for_user.md) <br>
- [README for Agents](references/README_for_agent.md) <br>
- [Practical Tips](references/TIPS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands and helper code for interacting with a user-operated TunnelProxy service; behavior depends on the configured host, port, token, timeout, and upload secret.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
