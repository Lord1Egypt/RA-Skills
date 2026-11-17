## Description:

Sync a Discord bot profile into an OpenClaw agent IDENTITY.md, save the avatar under workspace/avatars, and safely add Avatar and Discord metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xli](https://clawhub.ai/user/0xli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to synchronize a Discord bot profile into the current workspace identity file, including avatar and selected Discord metadata, without changing the Discord account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write sensitive or free-form Discord profile data into a persistent agent identity file.

Mitigation: Use a dedicated workspace and bot token, inspect the IDENTITY.md diff before reuse, and avoid storing email or bio unless required.

Risk: Explicit config or identity paths could target files outside the intended workspace.

Mitigation: Keep --config and --identity paths inside the intended workspace and review path choices before running automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xli/skills/sync-discord-identity)
- [Project homepage](https://github.com/0xli/sync-discord-identity)
- [Discord current user API endpoint](https://discord.com/api/v10/users/@me)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown identity edits, local avatar file, and concise status text or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the Discord API using a bot token from the selected OpenClaw workspace and may create an IDENTITY.md backup before editing.]

## Skill Version(s):

0.1.1 (source: release evidence; artifact frontmatter is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
