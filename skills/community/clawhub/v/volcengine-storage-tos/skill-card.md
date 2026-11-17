## Description:

Object storage operations for Volcengine TOS. Use when users need upload/download/sync, bucket policy checks, signed URLs, or storage troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Volcengine TOS buckets and objects, including uploads, downloads, sync tasks, bucket policy checks, signed URLs, and storage troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on Volcengine TOS buckets and objects, including upload, download, sync, and signed URL workflows.

Mitigation: Use narrowly scoped credentials, review bucket and object paths before execution, and require explicit confirmation for delete or broad sync operations.

Risk: Object-storage operations can produce incorrect or unintended results when paths, regions, policies, or metadata are wrong.

Mitigation: Confirm bucket, region, object paths, authentication, and bucket policy before running operations, and return checksum or size verification where possible.

## Reference(s):

- [Sources](references/sources.md)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/volcengine-storage-tos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with operational steps, command guidance, and result manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include object keys, URLs, checksums, sizes, and permission-check results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
