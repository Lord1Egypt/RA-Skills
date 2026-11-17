## Description:

Save and load OpenClaw conversation context with /save and /load slash commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkyotnfjfbjnknh](https://clawhub.ai/user/jkyotnfjfbjnknh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use this plugin to save conversation context to local files, list saved contexts, reload saved messages into a later session, or delete saved contexts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved conversations are stored locally in plaintext and may contain sensitive user or assistant context.

Mitigation: Use only on trusted single-user OpenClaw installations, avoid saving secrets, and restrict file permissions on the saves directory.

Risk: Loose session scoping and context restoration can expose or replace conversation history.

Mitigation: Avoid shared gateways or multi-user deployments until session ownership checks and safer context restoration are added.

Risk: Saved contexts can be deleted through the load command path.

Mitigation: Require confirmation for destructive actions before relying on this plugin in operational environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkyotnfjfbjnknh/skills/save-load)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown command responses and local JSON save files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists user and assistant messages as local plaintext JSON files under ~/.openclaw/saves.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
