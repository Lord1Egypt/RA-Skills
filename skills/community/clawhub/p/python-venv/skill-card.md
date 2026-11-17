## Description:

Python environment management skill that detects project type and existing environments, recommends Python tooling by popularity, and minimizes user interruptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cikichen](https://clawhub.ai/user/cikichen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to choose, reuse, create, and troubleshoot Python virtual environments and dependency installation workflows for projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make environment-changing decisions with too little user confirmation.

Mitigation: Require confirmation before creating environments, deleting .venv, or installing dependencies from project files unless the user has already requested that exact action.

Risk: The skill documents remote uv installer commands that execute downloaded scripts.

Mitigation: Verify the installer source and contents separately before running curl-to-shell or Invoke-Expression commands; prefer already installed tools or the standard venv fallback when verification is not available.

Risk: Troubleshooting guidance includes deleting and recreating a corrupted virtual environment.

Mitigation: Confirm deletion with the user and preserve dependency files or recreation steps before removing an existing environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cikichen/skills/python-venv)
- [Python Virtual Environment - Common Patterns](references/patterns.md)
- [Python Virtual Environment - Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides decision guidance for Python environment selection, reuse, creation, dependency installation, and troubleshooting.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
