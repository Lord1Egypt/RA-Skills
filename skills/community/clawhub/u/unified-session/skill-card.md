## Description: <br>
Helps a personal OpenClaw user configure direct-message session routing so multiple chat channels share one continuous agent conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1052326311](https://clawhub.ai/user/1052326311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and personal bot operators use this skill to diagnose, configure, restart, and verify a unified session setup across webchat and messaging channels. It is intended for single-user deployments where cross-device continuity is more important than per-channel session isolation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Merging direct-message context across channels can expose one user's conversation history to anyone else who can DM the same bot. <br>
Mitigation: Use this skill only for a personal OpenClaw agent, confirm no other users can DM the bot, and keep or restore per-channel-peer isolation for shared or multi-user deployments. <br>
Risk: Changing OpenClaw session routing may disrupt existing channel behavior until the gateway is restarted and verified. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before editing, restart the OpenClaw gateway after configuration changes, and verify the unified session from each enabled channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1052326311/unified-session) <br>
- [Artifact README](README.md) <br>
- [Artifact skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; proposes edits to OpenClaw configuration and gateway restart/verification steps.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
