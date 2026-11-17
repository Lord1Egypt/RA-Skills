## Description:

OpenClaw 工作流快速入门指南 - 含业务流程处理（TaskFlow）与数字资源入库（ClawHub）的端到端实操步骤，适用于新用户在 30 分钟内完成从内容创作到资源发布的完整链路

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this guide to learn an end-to-end workflow for TaskFlow orchestration and ClawHub digital resource publishing. It provides reproducible steps, API examples, shell commands, and review checkpoints for onboarding and release preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide asks users to install the ClawHub CLI through npm, which can expose users to package-source or version mistakes.

Mitigation: Verify the clawhub npm package source and intended version before installation, and avoid running global npm installs with elevated privileges.

Risk: Publishing a skill or resource directory can accidentally expose local secrets or unintended files.

Mitigation: Review and scan the resource directory for secrets and unwanted files before running clawhub publish.

Risk: Broad update commands can change more installed resources than intended.

Mitigation: Use clawhub update --all only when intentionally updating all installed resources; otherwise update a specific skill.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Registry](https://clawhub.com)
- [Artifact Reference README](artifact/reference/README.md)
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/workflow-starter-guide)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guide with TypeScript examples, shell command snippets, and checklist tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language onboarding content for OpenClaw TaskFlow and ClawHub publishing workflows]

## Skill Version(s):

1.0.0 (source: server release evidence, skill metadata, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
