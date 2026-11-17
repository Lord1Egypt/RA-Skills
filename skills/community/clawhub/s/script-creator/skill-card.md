## Description:

Create and modify scripts in ~/.nanobot/workspace/test with strict Git versioning, isolated per-script repositories, confirmation before execution, progress reporting, and Python dependency management through ~/.nanobot/workspace/venv.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cadot-eu](https://clawhub.ai/user/cadot-eu)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create or modify scripts under a controlled workspace workflow with explicit user confirmation, per-script Git history, and Python dependency management through a shared virtual environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to create files and run shell commands in a user workspace.

Mitigation: Review planned file paths and commands before execution, and require paths to stay inside ~/.nanobot/workspace/test.

Risk: The skill can install Python packages into a shared virtual environment without pinned versions.

Mitigation: Use trusted and reviewed dependency names, pin package versions where possible, and consider per-script virtual environments for stronger isolation.

Risk: Unvalidated script names or dependency names could affect shell command behavior.

Mitigation: Validate names, quote shell arguments, and reject ambiguous or unsafe input before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cadot-eu/skills/script-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and code-oriented workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before creation or modification steps; no fixed token caps are specified.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
