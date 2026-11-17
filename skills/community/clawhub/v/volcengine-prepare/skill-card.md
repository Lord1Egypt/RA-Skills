## Description:

Analyzes a local directory or GitHub repository for Volcengine deployment readiness and recommends ECS, VKE, or veFaaS plus CLI or IaC resource management before deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess whether a repository has a concrete Volcengine deployment target, compare viable ECS, VKE, and veFaaS paths, and choose a CLI or IaC resource-management approach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository analysis may read real environment or production configuration files that contain secrets.

Mitigation: Run the skill against sanitized repositories or template configuration files, and require explicit consent before scanning sensitive config.

## Reference(s):

- [Deploy Mode Heuristics](references/deploy-mode-heuristics.md)
- [ClawHub Skill Page](https://clawhub.ai/volc-sdk-team/skills/volcengine-prepare)
- [Publisher Profile](https://clawhub.ai/user/volc-sdk-team)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON findings and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a concise deploy-choice JSON handoff when the workflow continues.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
