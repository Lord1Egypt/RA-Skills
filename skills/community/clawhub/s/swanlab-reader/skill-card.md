## Description:

Reads SwanLab experiment data when a user provides a SwanLab run URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckqiao](https://clawhub.ai/user/ckqiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML practitioners use this skill to inspect SwanLab projects and runs, view metrics and configuration, retrieve metric histories, generate ASCII trend plots, and compare multiple runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access SwanLab data available to the configured API key.

Mitigation: Install and run it only when that level of SwanLab access is acceptable for the workspace.

Risk: The API key may be stored in ~/.config/swanlab/key or entered through a shell command.

Mitigation: Prefer protected environment variables, secure the local key file, and avoid entering secrets in commands that may be saved in shell history.

## Reference(s):

- [SwanLab](https://swanlab.cn)
- [SwanLab Reader on ClawHub](https://clawhub.ai/ckqiao/skills/swanlab-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and terminal-style text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tabular run summaries, metric statistics, quick query commands, and ASCII trend plots.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
