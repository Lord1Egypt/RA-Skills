## Description: <br>
Configures multiple independent OpenClaw gateway instances with separate agents, workspaces, bots, cross-agent communication, and multi-port management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create and run multiple isolated OpenClaw gateway instances for separate agents, teams, workspaces, and Feishu-connected bots. It is intended for multi-agent task routing, independent bot identities, and local gateway operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports an embedded shared API key and plaintext local secrets in generated configuration. <br>
Mitigation: Remove and rotate the embedded key before trusted use, and store secrets with local access controls or a secret manager rather than committing or copying them in plaintext. <br>
Risk: The security guidance calls out copied skills and memory during gateway setup. <br>
Mitigation: Review selected skills and memory files before copying them into new agent workspaces, and avoid copying sensitive or unrelated data. <br>
Risk: The security guidance calls out public IP-discovery requests and persistent user-level services. <br>
Mitigation: Review outbound IP lookup behavior and generated systemd user services before running the wizard in production or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pikaqiuyaya/setup-multi-gateway) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [feishu-agent-send skill](https://clawhub.com/skills/feishu-agent-send) <br>
- [ClawHub skill marketplace](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, JSON configuration examples, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local OpenClaw gateway configuration, workspace copies, and user-level systemd services.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
