## Description: <br>
Explore capability boundaries of a target Skill, analyze optimization potential, generate an optimized version using Training-Free GRPO, and compile results into a structured report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t1ans1r](https://clawhub.ai/user/t1ans1r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use Skills Coach to generate test tasks, optimize target skills, compare original and optimized behavior, and produce structured evaluation reports while preserving the original skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run commands, install software, and call external AI services during optimization and evaluation. <br>
Mitigation: Run it only in a disposable workspace, VM, or container, and review the target skill and generated commands before execution. <br>
Risk: Automatic dependency installation and auto-fix behavior can change the local environment or generated skill files. <br>
Mitigation: Disable auto_install_deps and auto_fix unless those changes are explicitly intended, and inspect generated artifacts before accepting them. <br>
Risk: Target skills or workspaces may contain secrets or content that should not be sent to external AI services. <br>
Mitigation: Use clean test workspaces without secrets or private data, and use scoped disposable credentials when external API access is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/t1ans1r/skills-coach) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Training-Free GRPO notes](artifact/archive/docs/README_TRAINING_FREE_GRPO.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON metadata, generated skill files, shell commands, and configuration changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates versioned run directories with tasks, execution logs, optimization artifacts, reports, and an optimized skill copy when retained.] <br>

## Skill Version(s): <br>
2.3.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
