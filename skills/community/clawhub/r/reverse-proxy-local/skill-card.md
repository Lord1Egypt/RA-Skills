## Description: <br>
Connect OpenClaw to the internet via Tailscale Funnel for remote OpenAI-compatible API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsheasha](https://clawhub.ai/user/tsheasha) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to publish a local OpenClaw gateway through Tailscale Funnel, generate bearer-token credentials, and test or share remote chat-completions access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish a local OpenClaw API endpoint to the internet. <br>
Mitigation: Use it only when public remote access is intended, verify bearer-token authentication works, and disable Funnel when external access is no longer needed. <br>
Risk: Generated credentials are reusable and can grant API access to anyone who receives them. <br>
Mitigation: Keep credentials private, share them only with trusted users, and rotate the token after sharing or suspected exposure. <br>
Risk: The setup script may install or start Homebrew, Tailscale, and gateway services with elevated permissions. <br>
Mitigation: Review scripts before execution and install Homebrew and Tailscale separately when possible. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/tsheasha/reverse-proxy-local) <br>
- [Tailscale](https://tailscale.com) <br>
- [Tailscale admin machines](https://login.tailscale.com/admin/machines) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON credential examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands and local configuration steps for Tailscale Funnel, OpenClaw gateway settings, credential generation, connection status, disconnection, and API testing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
