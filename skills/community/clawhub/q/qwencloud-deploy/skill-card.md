## Description:

qwencloud-deploy deploys, publishes, updates, cleans up, and optionally configures HTTPS for local projects or Git repositories on Alibaba Cloud International using ROS-managed cloud resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to take a local project or Git repository online on Alibaba Cloud International, including resource planning, cost confirmation, deployment, health checks, state recording, hot updates, cleanup, and optional domain plus HTTPS setup.

### Deployment Geography for Use:

Global, using Alibaba Cloud International regions; the skill defaults deployments to ap-southeast-1 (Singapore).

## Known Risks and Mitigations:

Risk: The skill can create, modify, and delete Alibaba Cloud resources and may be configured with broad cloud permissions.

Mitigation: Use the least-privilege RAM actions documented in the skill, review cost and resource confirmations before approval, and remove unused resources through the provided cleanup flow.

Risk: The skill runs commands on ECS instances and deploys user-provided application code.

Mitigation: Deploy only trusted projects, review generated plans before approving execution, and avoid running untrusted application code until the service is configured to run as a non-root user.

Risk: Deployment state files may contain signed artifact URLs and a local sidecar may contain ECS or database passwords.

Mitigation: Keep .qwencloud-deploy and .qwencloud-deploy.local uncommitted with restrictive file permissions, and remove or rotate stored passwords when they are no longer needed.

Risk: Domain registration and HTTPS setup can create billable or externally visible changes.

Mitigation: Require explicit user confirmation for domain purchase and DNS changes, and verify authoritative provider pricing before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cuixiaoyang123/skills/qwencloud-deploy)
- [Alibaba Cloud CLI installation guide](https://www.alibabacloud.com/help/en/cli/install-update-alibaba-cloud-cli)
- [Environment check](artifact/reference/deploy/01_env_check.md)
- [RAM policies](artifact/reference/rules/ram_policies.md)
- [Cost estimation](artifact/reference/deploy/09_estimate_cost.md)
- [HTTPS setup](artifact/reference/https/https_setup.md)
- [Cleanup](artifact/reference/cleanup/delete_stack.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown guidance with shell command execution, generated ROS/userdata configuration files, and JSON deployment state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates cloud resources and writes deployment state files, including a local password sidecar when deployment succeeds.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter says 2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
