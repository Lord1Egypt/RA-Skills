## Description:

An intelligent digital archivist skill for OpenClaw agents that monitors chat groups, captures memorable text and media, generates context-aware summaries, and stores them through the local Remember When CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericmora](https://clawhub.ai/user/ericmora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an OpenClaw agent identify memorable conversation content, summarize it, and archive text or media to local Remember When storage with group context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can monitor chats and retain summaries and media, which may capture sensitive personal or group information.

Mitigation: Require explicit per-group consent before archiving, show what will be saved, and provide clear deletion and export procedures.

Risk: The skill asks for shell execution and depends on the local remember-when CLI, so unsafe or unpinned CLI behavior could affect local storage.

Mitigation: Install a pinned and audited CLI release, restrict shell permissions to the required remember-when commands, and review commands before execution.

Risk: Heartbeat scanning and enrichment can create ongoing background collection and may perform external searches despite the local-only privacy claim.

Mitigation: Disable heartbeat and enrichment by default, enable them only after user approval, and clearly label any external search-derived context before storing it.

## Reference(s):

- [Remember When Skill on ClawHub](https://clawhub.ai/ericmora/skills/remember-when-skill)
- [Publisher profile](https://clawhub.ai/user/ericmora)
- [Remember When homepage](https://remember-when.agentic.2mes4.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, group names, entry metadata, and confirmation prompts for archiving actions.]

## Skill Version(s):

1.2.3 (source: server release metadata and package.json; SKILL.md lists 1.2.0 and CHANGELOG top entry lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
