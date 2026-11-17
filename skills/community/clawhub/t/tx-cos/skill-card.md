## Description:

Helps OpenClaw agents operate Tencent Cloud COS for uploads, batch syncs, multipart large-file uploads, signed URLs, object browsing, object management, folder statistics, and COS configuration checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent perform common Tencent Cloud COS storage workflows, including file uploads, temporary sharing links, object listing and management, folder deletion, storage statistics, and configuration troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently delete, move, rename, or recursively remove Tencent COS objects.

Mitigation: Use least-privileged COS credentials, enable bucket versioning or retention where possible, and manually verify object keys, prefixes, and deletion scope before execution.

Risk: The skill can generate signed URLs that expose COS objects.

Mitigation: Confirm the target object and expiration period before sharing signed URLs, and avoid using production buckets unless necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/156554395/skills/tx-cos)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js scripts that require Tencent Cloud COS credentials and bucket configuration.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
