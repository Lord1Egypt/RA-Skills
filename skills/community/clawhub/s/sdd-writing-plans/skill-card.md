## Description:

当有规格说明或需要多步骤任务的需求时，在编写代码之前使用。根据 spec-design.md 生成可执行的 spec-plan.md。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill in OpenClaw SDD workflows to turn an existing spec-design.md into a concise spec-plan.md with implementation tasks and executable validation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated implementation plan may contain incorrect, incomplete, or misleading tasks for the project.

Mitigation: Review the generated summary, task list, file list, and validation commands before confirming the write step.

Risk: The skill may inspect relevant project files and create a plan file in the selected spec directory.

Mitigation: Run it only in the intended workspace and confirm the target spec-design.md path before allowing spec-plan.md to be written.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown file with task checklists and inline CLI validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces spec-plan.md in the same directory as the source spec-design.md after user confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
