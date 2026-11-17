## Description:

Query documents on your NFS shares, SMB servers, or local drive using local AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zettabrain](https://clawhub.ai/user/zettabrain)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and teams use this skill to chat with and index documents from local folders, NFS, SMB, or S3-backed sources through a local RAG workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions may run remote or unpinned code with elevated privileges.

Mitigation: Review installer source before use and prefer a pinned, verifiable package or installer with checksum or signature verification.

Risk: Setup can create an auto-starting local service.

Mitigation: Install only when that persistence is acceptable, and use the documented service controls to stop, disable, or remove it when no longer needed.

Risk: Configured document sources may include local folders, network shares, or S3 sources.

Mitigation: Verify selected folders, shares, and object-storage locations before ingestion so only intended documents are indexed.

Risk: A remote OLLAMA_HOST can send document queries and retrieved chunks off-machine.

Mitigation: Keep OLLAMA_HOST pointed at localhost when document queries must remain on-device.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zettabrain/skills/zettabrain-rag)
- [ZettaBrain Website](https://zettabrain.io)
- [GitHub Source](https://github.com/zettabrain/zettabrain-rag)
- [PyPI Package](https://pypi.org/project/zettabrain-rag/)
- [Linux and macOS Installer](https://github.com/zettabrain/zettabrain-rag/blob/main/install.sh)
- [Windows Installer](https://github.com/zettabrain/zettabrain-rag/blob/main/install.ps1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local document-chat setup, ingestion, service-management, and privacy guidance for an agent to follow.]

## Skill Version(s):

1.0.2 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
