## Description:

skill-python-env provides an internal Python virtual environment helper for other skills, creating shared versioned environments under ~/.python_env/<version> and installing uv automatically when missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other skill authors use this internal utility to prepare reusable Python virtual environments by version and optionally install packages before running Python-based skill workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install uv by executing live remote installer scripts.

Mitigation: Preinstall uv from a trusted source or review the installer path and network behavior before allowing the skill to run.

Risk: The virtual environment path is derived from the requested Python version and incomplete environments may be recursively deleted.

Mitigation: Accept only plain Python version values such as 3.11 or 3.12 and restrict deletion to verified directories under ~/.python_env.

Risk: Callers can request package installation into the shared environment.

Mitigation: Limit callers to trusted skills and restrict package names to approved dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liberalchang/skills/skill-python-env)
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text logs with machine-readable environment lines and Markdown documentation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs activation path, environment directory, and Python version for caller parsing.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
