## Description:

Posts a message with optional attachments to a Discord channel through a channel webhook after the user approves it. Use when the user wants to post an announcement or update to their Discord server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Discord server owners and their agents use this skill to prepare and publish an approved announcement or update with optional attachments to a channel. The user reviews the exact post and approves publication in their own terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The channel webhook URL can post to its configured channel if exposed.

Mitigation: Keep the webhook secret and limited to the intended channel; rotate it if it leaks.

Risk: The separate socialkit-social-core dependency is outside this release's security review.

Mitigation: Review that dependency before use, inspect the exact message and attachments, and approve them yourself in your terminal.

## Reference(s):

- [Discord setup](references/setup.md)
- [Discord webhook documentation](https://docs.discord.com/developers/resources/webhook)
- [ClawHub skill release](https://clawhub.ai/ahmadhussain0335/skills/socialkit-discord-post)

## Skill Output:

**Output Type(s):** [Text, Configuration, Files]

**Output Format:** [Discord message text with optional local file attachments, plus a JSON post configuration and Markdown approval preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts to one configured channel webhook after user approval; mentions are disabled by default.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
