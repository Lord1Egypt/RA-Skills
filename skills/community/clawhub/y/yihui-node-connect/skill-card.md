## Description: <br>
Diagnose OpenClaw node connection and pairing failures for Android, iOS, and macOS companion apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot OpenClaw node-to-gateway connectivity, setup-code routing, and device pairing problems across LAN, tailnet, public URL, and remote gateway setups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Device approval commands can authorize a pending OpenClaw device to connect. <br>
Mitigation: Review the pending device and any proposed approval command before running it, especially openclaw devices approve --latest. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1yihui/yihui-node-connect) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Troubleshooting guidance asks for clarifying setup details when the connection route or app error is ambiguous.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
