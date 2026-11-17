## Description:

Browse categories, preview, apply, and restore OpenClaw SOUL.md personas from a curated remote catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexleach](https://clawhub.ai/user/alexleach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to browse OpenClaw persona categories, inspect available SOUL.md personas, apply one to the current workspace, and restore a previous persona from backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying a persona can replace the workspace SOUL.md with unverified remote content and affect future agent sessions.

Mitigation: Review persona content and catalog source before applying it, use only trusted catalog entries, and start a new session only after confirming the change.

Risk: Apply and restore commands modify local workspace files.

Mitigation: Keep an independent backup and verify the generated soul-data/backups/ and soul-data/state.json records before relying on a restored or newly applied persona.

Risk: The security scan verdict is suspicious because remote content sources are broader than the safety rules describe.

Mitigation: Install only when the publisher and catalog sources are trusted, and avoid sensitive workspaces unless the persona content has been reviewed first.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexleach/skills/soul-search)
- [Default Persona Catalog](https://raw.githubusercontent.com/mergisi/awesome-openclaw-agents/refs/heads/main/agents.json)
- [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents)
- [OpenClaw SOUL.md Template](https://github.com/openclaw/openclaw/blob/main/docs/reference/templates/SOUL.md)
- [Artifact Sources](artifact/references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Plain text and Markdown command output, with local SOUL.md, backup, cache, and state files when apply or restore commands are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; apply and restore operations can modify workspace persona configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
