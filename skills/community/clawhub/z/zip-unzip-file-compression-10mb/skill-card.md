## Description:

Compresses and decompresses ZIP and GZIP archives up to 10MB for AgentPMT-hosted agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to bundle reports, code outputs, logs, or data exports into ZIP/GZIP archives and to extract uploaded archives for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected file contents may be sent to AgentPMT during compression or decompression.

Mitigation: Keep inputs scoped to the minimum needed and avoid sending sensitive files unless the deployment owner accepts the data handling risk.

Risk: Outputs and extracted files are stored in cloud storage by default and made available through signed URLs.

Mitigation: Use store_file: false when inline output is sufficient, and account for the default 7-day retention when handling non-public data.

Risk: The security verdict is suspicious because the skill can send arbitrary file contents to a remote service.

Mitigation: Review the setup path before deployment, avoid broad automatic invocation, and prefer pinned or reviewed installation commands.

## Reference(s):

- [Action schema](artifact/schema.md)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/zip-unzip-file-compression-10mb)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/zip-unzip-file-compression-10mb)

## Skill Output:

**Output Type(s):** [Files, JSON, Guidance]

**Output Format:** [JSON responses containing file IDs, signed URLs, and optional base64 file contents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports ZIP and GZIP up to 10MB; ZIP archives support up to 200 files; stored files expire after 7 days by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
