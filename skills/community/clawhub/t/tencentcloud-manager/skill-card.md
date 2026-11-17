## Description:

TencentCloud Manager helps agents manage Tencent Cloud CVM, Lighthouse, and COS resources, including setup, provisioning, operations, and cost review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to configure and manage Tencent Cloud CVM, Lighthouse, and COS resources, including provisioning, status checks, instance lifecycle operations, storage lifecycle setup, and cost-oriented resource review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Tencent Cloud permissions can allow resource creation, instance lifecycle changes, and object storage writes or deletes.

Mitigation: Review and narrow the CAM policy before use; use a dedicated sub-user and scope permissions to specific resources or buckets wherever possible.

Risk: Long-lived Tencent Cloud credentials are configured through environment variables and .env files.

Mitigation: Keep credentials out of Git, avoid printing or sharing .env contents, and rotate keys regularly.

Risk: The setup examples install Python dependencies with --break-system-packages.

Mitigation: Prefer a virtual environment with pinned dependencies for installation and execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/tencentcloud-manager)
- [Tencent Cloud CVM API documentation](https://cloud.tencent.com/document/api/213)
- [Tencent Cloud Lighthouse API documentation](https://cloud.tencent.com/document/api/1170)
- [Tencent Cloud COS API documentation](https://cloud.tencent.com/document/api/436)
- [Tencent Cloud CAM permission configuration](https://cloud.tencent.com/document/product/598/10603)
- [Permission policy guide](docs/permission-policy.md)
- [Quick reference](docs/quick-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Tencent Cloud API actions that create, modify, start, stop, restart, or upload resources.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
