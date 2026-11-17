## Description:

Use when interacting with a Trilium Notes server via the ETAPI REST API for creating, reading, updating, searching, or deleting notes, branches, attributes, attachments, day/week/month notes, obtaining auth tokens, or scripting Trilium operations from the shell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanickxia](https://clawhub.ai/user/yanickxia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to script authenticated Trilium ETAPI workflows, including note creation, metadata updates, search, import/export, backups, and integration debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents authenticated ETAPI operations that can modify or delete Trilium notes, branches, attributes, and attachments.

Mitigation: Require explicit confirmation before destructive operations and verify the target IDs before issuing DELETE or overwrite commands.

Risk: ETAPI tokens and passwords grant access to Trilium data if exposed.

Mitigation: Treat TRILIUM_TOKEN and passwords as secrets, avoid logging them, and use HTTPS for remote servers.

Risk: Export and backup workflows can expose note contents or write server-side backup files.

Mitigation: Review export destinations, backup names, and access permissions before running export or backup commands.

## Reference(s):

- [Trilium ETAPI endpoint reference](api-reference.md)
- [ClawHub skill page](https://clawhub.ai/yanickxia/skills/trilium-etapi)
- [trilium-py client](https://github.com/Nriver/trilium-py)
- [trilium-client Python package](https://pypi.org/project/trilium-client/)
- [trilium-api TypeScript package](https://www.npmjs.com/package/trilium-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, curl, jq, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides examples and operational guidance; it does not directly execute ETAPI calls.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
