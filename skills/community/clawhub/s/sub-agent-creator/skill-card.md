## Description: <br>
Creates OpenClaw agents by collecting setup details, scaffolding workspace files, copying runtime configuration, updating openclaw.json bindings, and restarting the gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lidian6864677](https://clawhub.ai/user/lidian6864677) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create a new assistant with an agent workspace, persona files, runtime configuration, optional Feishu bindings, and gateway activation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent local OpenClaw configuration changes and restart the gateway. <br>
Mitigation: Review the agent ID, Feishu peer IDs, and config changes before use, and keep the openclaw.json backup for rollback. <br>
Risk: Copying auth-profiles.json from the main agent can carry broad credentials or permissions into the new agent. <br>
Mitigation: Inspect the copied auth profile and prefer a least-privilege profile before enabling the new agent. <br>
Risk: Incorrect chat bindings can route messages to the wrong group or direct peer. <br>
Mitigation: Verify each peer ID and confirm the bot is intentionally added to the target group or direct chat. <br>


## Reference(s): <br>
- [SOUL.md Templates](references/soul_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and file-template snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local OpenClaw workspace and configuration files when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
