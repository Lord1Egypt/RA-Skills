## Description: <br>
Turns a Roborock vacuum into a conversational OpenClaw companion for natural-language status, docking, pause, whole-home cleaning, and room-specific cleaning commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[serdarsalim](https://clawhub.ai/user/serdarsalim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw and Telegram users use this skill to operate a Roborock vacuum through short conversational commands while keeping control scoped to Jojo-related vacuum tasks. It is intended for users who want room-aware vacuum control through an agent interface rather than raw CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad chat phrases can control a real Roborock vacuum. <br>
Mitigation: Use a dedicated Jojo or Telegram agent, or require explicit trigger phrases such as "Jojo, pause cleaning" before executing vacuum commands. <br>
Risk: The shell configuration path can execute local code if pointed at an untrusted file. <br>
Mitigation: Keep jojo.env private, restrict file permissions, and do not set JOJO_CONFIG_FILE to untrusted paths. <br>
Risk: Local configuration may expose device IDs or unrelated tokens if mishandled. <br>
Mitigation: Do not publish jojo.env, Telegram tokens, or device identifiers, and avoid storing unrelated secrets in the skill configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/serdarsalim/roborock-conversational-control) <br>
- [README](README.md) <br>
- [Setup guide](SETUP.md) <br>
- [Agent notes](AGENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and short device-focused responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Roborock CLI authentication and a private jojo.env configuration file with a device ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
