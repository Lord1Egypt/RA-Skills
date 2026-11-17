## Description:

SiYuan Note API client for complete notebook, document, block, search, export, and local API management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiwei2027](https://clawhub.ai/user/weiwei2027)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to let an agent manage a local SiYuan Note workspace. It supports listing, searching, reading, creating, updating, moving, deleting, and exporting notebooks, documents, blocks, assets, and files through the SiYuan local HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit, move, or delete notebooks, documents, blocks, and files in a SiYuan workspace.

Mitigation: Back up notes before write/delete operations and review the exact target IDs, paths, and command flags before execution.

Risk: The skill depends on config.yaml containing a SiYuan API token.

Mitigation: Protect config.yaml, avoid sharing logs or artifacts that expose the token, and rotate the token if it may have been disclosed.

Risk: Raw SQL, forward_proxy, file deletion, and --yes can perform broad or irreversible actions.

Mitigation: Use these capabilities only with explicit intent, keep base_url pointed at a trusted localhost SiYuan instance, and prefer confirmation prompts for destructive commands.

## Reference(s):

- [ClawHub SiYuan release page](https://clawhub.ai/weiwei2027/skills/siyuan)
- [SiYuan official repository](https://github.com/siyuan-note/siyuan)
- [SiYuan online API documentation](https://www.siyuan-note.club/apis)
- [SiYuan API.md source](https://github.com/siyuan-note/siyuan/blob/master/API.md)
- [Artifact API reference](artifact/API.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, terminal text, and Python API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local SiYuan API endpoint and token in config.yaml; operations may read, create, update, delete, move, export, query, or proxy through that local instance.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter, evidence.release.version, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
