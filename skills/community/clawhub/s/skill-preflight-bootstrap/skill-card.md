## Description:

Bootstraps a repository-level workflow that reminds agents to check available skills before starting work and installs supporting project hooks, learning logs, and usage documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sysundy](https://clawhub.ai/user/sysundy)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to initialize new repositories with a repeatable skill-preflight workflow, including local skill search scripts, project-level Codex and Claude hook settings, learning logs, and team usage guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project hooks and AGENTS.md changes can alter future agent behavior in the repository.

Mitigation: Run the bootstrap script with --dry-run first and review the planned changes to AGENTS.md, .codex/settings.json, and .claude/settings.json before installing.

Risk: Remote skill search can invoke an unpinned npm package through npx.

Mitigation: Avoid remote search unless the npm skills package source is trusted, or replace the command with a pinned or internally approved alternative.

Risk: Shared repositories may need a rollback path for generated scripts, hooks, and documentation.

Mitigation: Review the generated files before committing and define an uninstall or rollback process before broad team adoption.

## Reference(s):

- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated repository files when the bootstrap script is executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes project-level scripts, hook settings, learning logs, documentation, and an AGENTS.md section; supports dry-run and force modes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
