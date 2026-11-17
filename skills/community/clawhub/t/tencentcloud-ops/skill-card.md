## Description:

TencentCloud OPS helps agents create, manage, monitor, and secure Tencent Cloud CVM servers and COS buckets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to generate guidance, Python examples, shell commands, and configuration steps for Tencent Cloud CVM and COS operations, including provisioning, deletion, file transfer, cost controls, and security setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Tencent Cloud permissions could allow unintended resource creation, deletion, network changes, or storage access.

Mitigation: Use a dedicated non-production Tencent Cloud sub-user and replace wildcard policies with narrow actions and resource scopes before use.

Risk: Destructive CVM and COS operations may remove cloud resources if targets are not independently checked.

Mitigation: Separately verify every target resource before running deletion, shutdown, or bucket removal operations.

Risk: Credential exposure could occur if .env contents or Tencent Cloud keys are printed, shared, or committed.

Mitigation: Keep .env files out of source control, avoid printing credential values, and rotate keys regularly.

Risk: Unpinned dependencies may change behavior across installs.

Mitigation: Install dependencies in a virtual environment with pinned versions.

## Reference(s):

- [TencentCloud OPS ClawHub page](https://clawhub.ai/ugpoor/skills/tencentcloud-ops)
- [Tencent Cloud API documentation](https://cloud.tencent.com/document/api)
- [Tencent Cloud CVM API](https://cloud.tencent.com/document/api/213)
- [Tencent Cloud COS API](https://cloud.tencent.com/document/api/436)
- [Tencent Cloud CAM user management](https://cloud.tencent.com/document/product/598)
- [Tencent Cloud API 3.0 Explorer](https://console.cloud.tencent.com/api/explorer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Tencent Cloud API operations that require credentialed execution outside the agent response.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
