## Description:

Skill Orchestration Core helps agents manage shared project context, orchestrate DESIGN.md workflows, validate expected outputs, and reuse workflow templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multi-step development workflows, pass context between skills, validate generated outputs, and start from reusable project templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-controlled DESIGN.md files can strongly influence delegated agent work and file writes.

Mitigation: Use only trusted or reviewed DESIGN.md files, constrain delegated agent tools to the project root, and require user approval before granting broad terminal, file, or web access.

Risk: Auto-fix behavior can create placeholder files or modify expected outputs.

Mitigation: Run auto-fix only in a version-controlled project and review the resulting diff before continuing the workflow.

Risk: Most documentation and command output are Chinese, which can cause review or operating mistakes for non-Chinese readers.

Mitigation: Assign reviewers or operators who can read the documentation, or translate the relevant workflow instructions before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fish1981bimmer/skills/skill-orchestration-core)
- [Workflow Orchestrator Regex Pitfalls](references/workflow-orchestrator-regex-pitfalls.md)
- [Template Authoring and Recovery](references/template-authoring-and-recovery.md)
- [Workflow Templates README](templates/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, YAML, and shell command text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update orchestration context, state, checkpoint, and placeholder output files when invoked with write-oriented commands.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
