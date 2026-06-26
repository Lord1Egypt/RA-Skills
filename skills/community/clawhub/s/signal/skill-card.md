## Description: <br>
Provides guidance for using OpenClaw's Signal channel via signal-cli to send messages and reactions, manage DM and group behavior, and configure channel safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blake-lucas](https://clawhub.ai/user/blake-lucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate OpenClaw's Signal channel, including sending messages and reactions, approving DM pairings, and applying group-chat safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to connect OpenClaw to a Signal account that can send messages and reactions. <br>
Mitigation: Use a dedicated bot number, keep DM and group allowlists narrow, and review signal-cli download commands before running them. <br>
Risk: Signal-based configuration writes can change channel behavior when enabled. <br>
Mitigation: Disable configWrites unless specifically needed and require explicit owner confirmation for destructive or externally visible group requests. <br>


## Reference(s): <br>
- [ClawHub Signal Skill](https://clawhub.ai/blake-lucas/signal) <br>
- [OpenClaw Signal docs](https://docs.openclaw.ai/channels/signal) <br>
- [signal-cli project and docs](https://github.com/AsamK/signal-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Signal command examples, setup diagnostics, and operational safeguards.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
