## Description:

Organizes research workspaces across local files, Zotero, Obsidian, and Feishu using a single source of truth for each type of content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomuiv](https://clawhub.ai/user/tomuiv)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and research teams use this skill to structure projects, map resources across tools, archive conversations, and coordinate file handoffs and cross-device synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled credential vault can access sensitive credentials and master keys.

Mitigation: Review the vault's key storage before use and store credentials only when this behavior is intended.

Risk: Optional credential hooks can run commands after credentials change.

Mitigation: Do not add hooks.json unless every configured command is trusted.

## Reference(s):

- [research-ops on ClawHub](https://clawhub.ai/tomuiv/skills/research-ops)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance, project files, and JSON script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific paths and tool mappings are supplied by the user's workspace.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; bundled SKILL.md lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
