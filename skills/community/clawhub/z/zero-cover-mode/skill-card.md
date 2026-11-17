## Description:

Zero Cover Mode helps agents run a structured bug-fix closure workflow with environment detection, root-cause analysis, regression testing, fix archiving, weekly reporting, and repeat-bug refactoring alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xincen0725](https://clawhub.ai/user/xincen0725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to make bug fixes follow a repeatable closure process: detect the project environment, document root cause, add or run regression tests, archive evidence, and surface recurring bug patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes workflow state, bug evidence, closure logs, reports, and related files into the workspace.

Mitigation: Run it in a controlled workspace, review the target paths before use, and avoid workspaces where a bugs directory contains unrelated data.

Risk: The skill can run project test commands as part of the bug-fix workflow.

Mitigation: Review detected or supplied test commands before execution and use a sandbox for untrusted repositories.

Risk: The skill may create future verification tasks through generated cron instructions.

Mitigation: Inspect generated cron instructions manually and enable only the checks that match the repository's operational policy.

Risk: The security scan flags dynamic imports and cleanup behavior as items requiring installation review.

Mitigation: Review the artifact before installation, keep backups or version control available, and restrict use to repositories where the cleanup scope is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xincen0725/skills/zero-cover-mode)
- [Publisher profile](https://clawhub.ai/user/xincen0725)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown workflow guidance with Python and shell command examples; supporting scripts produce JSON, NDJSON, logs, reports, and regression test files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write bug-specific evidence directories, workspace state files, closure logs, refactoring alerts, reports, and cron instruction JSON.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and pyproject.toml report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
