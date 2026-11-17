## Description:

Provides Tencent Cloud COS bucket and object management guidance and Python utilities for upload, download, lifecycle configuration, access control, and storage cost estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to configure Tencent Cloud COS credentials, manage buckets and objects, apply lifecycle policies, and estimate storage-class costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends account-wide COS permissions, which can grant broader storage access than a specific task requires.

Mitigation: Use a dedicated Tencent Cloud sub-user with bucket- and prefix-scoped least-privilege policies, and avoid wildcard COS permissions.

Risk: Bucket and object deletion, including force-delete behavior, can permanently remove stored data.

Mitigation: Review the target bucket, prefix, and object keys before execution; use backups or versioning where appropriate, and require explicit operator approval for destructive actions.

Risk: Credential setup examples involve local environment files that may expose secrets if displayed or shared.

Mitigation: Store credentials in protected environment configuration, avoid printing `.env` contents, and rotate exposed Tencent Cloud keys immediately.

Risk: Unpinned dependency installation can introduce supply-chain or compatibility risk.

Mitigation: Install dependencies in a virtual environment with reviewed, pinned versions before using the skill with production resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/tencentcloud-cos-manager)
- [Tencent Cloud COS API documentation](https://cloud.tencent.com/document/api/436)
- [Tencent Cloud COS storage class documentation](https://cloud.tencent.com/document/product/436/33417)
- [Tencent Cloud COS lifecycle management documentation](https://cloud.tencent.com/document/product/436/30688)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; Python utilities return dictionaries, lists, strings, or console output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Tencent Cloud credentials from environment variables and can issue Tencent COS API calls when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact src/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
