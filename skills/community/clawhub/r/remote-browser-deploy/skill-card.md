## Description: <br>
Deploys a visible remote browser environment using noVNC, Chromium, and Chrome DevTools Protocol on Linux, or attaches to a local Edge or Chrome browser over CDP on Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to set up a shared visual browser session for login flows, verification challenges, content publishing, and webpage debugging where the user and agent need to see the same browser state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Linux deployment requires broad root or sudo privileges. <br>
Mitigation: Run it only on a machine or VM you administer, avoid blanket passwordless sudo, and remove any temporary sudoers entry immediately after setup. <br>
Risk: The noVNC service can expose a persistent remote browser interface on port 6080. <br>
Mitigation: Avoid public internet exposure unless protected by controls such as a firewall allowlist, VPN, SSH tunnel, TLS/authenticated proxy, and a stronger password. <br>
Risk: The deployment creates persistent system services and a browser profile under /root. <br>
Mitigation: Review enabled services and disable or remove them, along with the /root browser profile, when remote browser access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/remote-browser-deploy) <br>
- [noVNC repository](https://github.com/novnc/noVNC.git) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment steps, service configuration, validation commands, troubleshooting guidance, and completion-message templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
