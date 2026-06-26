## Description: <br>
Sync a Discord bot profile into an OpenClaw agent IDENTITY.md, save the avatar under workspace/avatars, and safely add Avatar and Discord metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xli](https://clawhub.ai/user/0xli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to synchronize Discord bot identity data into a local workspace identity file and avatar directory while preserving unrelated identity content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a Discord bot token from the selected workspace's openclaw.json. <br>
Mitigation: Verify the workspace path and channel selection before use, do not echo tokens, and rotate any token that has been exposed. <br>
Risk: Discord email or bio metadata may be written into IDENTITY.md when present. <br>
Mitigation: Store only metadata intentionally meant to be available to tools or users who can read or share the workspace. <br>
Risk: An existing Avatar field can be replaced when forced. <br>
Mitigation: Review the current avatar value first and use force replacement only when the Discord avatar should become authoritative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xli/sync-discord-identity) <br>
- [Project homepage](https://github.com/0xli/sync-discord-identity) <br>
- [Discord user profile API](https://discord.com/api/v10/users/@me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional Python command execution and local file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update IDENTITY.md, save an avatar file under workspace/avatars, and print local paths and avatar URL.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
