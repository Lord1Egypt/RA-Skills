## Description:

Prioritize uv over pip for Python package management and execution, routing Python commands and CLI tools through uv run or uvx.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcoracer](https://clawhub.ai/user/marcoracer)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill when working on Python projects to choose uv-based commands for dependency installation, virtual environments, CLI tools, tests, dbt, and other Python tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on uv routing can conflict with pinned, offline, hermetic, or non-uv Python workflows.

Mitigation: Review affected projects before installation and follow project-managed tooling or lockfiles when they define the Python workflow.

Risk: Unpinned uvx or @latest commands can execute tool versions that differ over time.

Mitigation: Prefer project-managed locked tools or explicit versions for repeatable linting, formatting, test, and utility commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcoracer/skills/uv-priority)
- [Project homepage](https://github.com/marcoracer/uv-priority)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv to be available; the skill is always-on for Python-related tasks.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
