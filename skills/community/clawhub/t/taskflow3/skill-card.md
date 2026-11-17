## Description:

TaskFlow 3.0 helps agents run project-based workflows from PROJECT.yaml files, check scheduling constraints, and record execution status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manwjh](https://clawhub.ai/user/manwjh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect TaskFlow project configurations, choose eligible projects, execute ordered workflow steps, and update project and global execution records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to read local project memory or intelligence files.

Mitigation: Run it in a contained workspace and review PROJECT.yaml paths before granting access.

Risk: Configured workflows may publish or republish derived content externally without clear approval controls.

Mitigation: Require a human preview and approval before browser-based or platform publication steps.

Risk: Project configuration can drive file paths and workflow actions.

Mitigation: Inspect PROJECT.yaml for unexpected targets, source paths, and workflow steps before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/manwjh/skills/taskflow3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON/YAML configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct file reads and writes in a local TaskFlow workspace and should be reviewed before publication workflows run.]

## Skill Version(s):

3.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
