## Description: <br>
Fixes WhatsApp Web status 428 connection issues for OpenClaw by providing proxy configuration guidance and an optional repair script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffreyCheungRT](https://clawhub.ai/user/jeffreyCheungRT) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an OpenClaw WhatsApp gateway reports status 428, needs proxy configuration, or requires post-deployment connection recovery steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent local changes to OpenClaw package files and the user systemd service. <br>
Mitigation: Back up the service file and installed package files before use, run during a maintenance window, and keep a rollback path ready. <br>
Risk: The fix routes WhatsApp traffic through a configured proxy endpoint. <br>
Mitigation: Verify the proxy operator and endpoint before use, and only route traffic through a proxy trusted for the deployment. <br>
Risk: Gateway restart and proxy changes may affect messaging connectivity or behavior. <br>
Mitigation: Review the script before running it, monitor gateway logs and channel status after restart, and roll back if connectivity changes unexpectedly. <br>


## Reference(s): <br>
- [WhatsApp 428 detailed reference](references/quick-ref.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an optional bash script that accepts a proxy port argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
