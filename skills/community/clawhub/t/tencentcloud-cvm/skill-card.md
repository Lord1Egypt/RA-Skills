## Description:

Helps agents create, inspect, operate, and manage Tencent Cloud CVM instances, including promotional plan lookup, cost controls, and security group setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to guide Tencent Cloud CVM setup and operations, including instance lifecycle management, plan selection, cost-aware shutdown guidance, and security group configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Tencent Cloud permissions can allow more CVM, VPC, or disk actions than an agent actually needs.

Mitigation: Use a dedicated low-privilege Tencent Cloud sub-user and replace wildcard permissions with a narrow allowlist before installing or running the skill.

Risk: Credential handling guidance may expose Tencent Cloud API secrets through config files, terminal output, or shared logs.

Mitigation: Never print or share config/.env values, keep credentials out of version control, and rotate dedicated credentials regularly.

Risk: Lifecycle actions can create paid resources or delete running instances.

Mitigation: Require explicit human approval before creating prepaid resources, stopping production instances, or deleting instances.

Risk: Unpinned dependency installation can introduce unexpected package changes.

Mitigation: Install dependencies in a pinned virtual environment that is reviewed before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/tencentcloud-cvm)
- [Tencent Cloud CVM API documentation](https://cloud.tencent.com/document/api/213)
- [Tencent Cloud CVM product documentation](https://cloud.tencent.com/document/product/213)
- [Tencent Cloud CAM user management documentation](https://cloud.tencent.com/document/product/598)
- [Tencent Cloud API Explorer](https://console.cloud.tencent.com/api/explorer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials and environment variables; proposed actions can create, stop, restart, or delete cloud resources.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
