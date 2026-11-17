## Description:

Tracks the ZLMediaKit repository, summarizes recent issues and pull requests, and helps analyze ZLMediaKit source code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feixintianxia](https://clawhub.ai/user/feixintianxia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to follow ZLMediaKit project activity, clone or update the local repository, inspect recent GitHub issues and pull requests, and produce Markdown source-analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script has a shell-command injection risk through the workspace path.

Mitigation: Review and fix the shell=True command construction before normal use, or run the script only in a tightly controlled workspace with a trusted WORKSPACE_DIR.

Risk: The skill clones or updates a local copy of ZLMediaKit and queries GitHub.

Mitigation: Install only where repository writes and GitHub network access are acceptable, and use a least-privilege GitHub token only when needed.

Risk: Scheduled runs can repeatedly execute repository update and reporting commands.

Mitigation: Avoid scheduled execution until the command-injection issue is corrected and the workspace path is controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feixintianxia/skills/zlmediakit)
- [ZLMediaKit repository](https://github.com/ZLMediaKit/ZLMediaKit)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown reports with inline shell commands and source-code path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local zlmediakit_report.md report after cloning or updating the ZLMediaKit repository.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
