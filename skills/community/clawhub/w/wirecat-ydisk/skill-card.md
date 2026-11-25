## Description:

Use ydisk to search and read the owner's Yandex Disk files and to list, download, upload, move or share them. Use when a task needs a file or a fact from Yandex Disk (Яндекс Диск), or a change to files there.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can use this skill to find and read information in their Yandex Disk, manage files and folders, and edit supported text and office documents. It also guides agents through synchronization and sharing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented operations can delete files, empty the trash, overwrite resources, or publish public links.

Mitigation: Confirm the target and intended sharing audience with the owner before these actions; use --dry-run when a write is uncertain.

## Reference(s):

- [Yandex Disk API overview](artifact/references/api.md)
- [Disk API](artifact/references/api/api-disk.md)
- [Disk resource API](artifact/references/api/api-disk-resources.md)
- [Public resource API](artifact/references/api/api-disk-public-resources.md)
- [Trash resource API](artifact/references/api/api-disk-trash-resources.md)
- [Asynchronous operation API](artifact/references/api/api-diREDACTED-SECRET.md)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, JSON]

**Output Format:** [JSON command responses and file content, with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file contents, search excerpts, metadata, or results of file operations.]

## Skill Version(s):

1.0.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
