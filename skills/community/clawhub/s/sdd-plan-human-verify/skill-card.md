## Description:

从已完成的 spec-plan.md 生成验收清单，包含 [A]/[H] 子步骤，覆盖所有验证项用于 AI 驱动验收。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn SDD plan and design documents into a detailed human verification checklist with automated and manual acceptance steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can convert project specification text into commands intended for later autonomous execution.

Mitigation: Install only if you trust the spec documents that this skill will read and are prepared to review every generated [A], [AUTO], and [AUTO/SERVICE] command before running sdd-start-human-verify. Pay special attention to commands that install packages, contact the network, read .env files, start services, or modify databases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mahingbun-dev/skills/sdd-plan-human-verify)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown checklist with inline shell commands and yes/no human verification prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces spec-human-verify.md content in Chinese after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
