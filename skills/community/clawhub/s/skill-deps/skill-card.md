## Description:

Track and manage dependencies between OpenClaw skills by scanning dependencies, visualizing skill trees, detecting circular dependencies, and managing skill versioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myrodar](https://clawhub.ai/user/myrodar)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to inspect OpenClaw skill dependency metadata, visualize dependency trees, detect missing dependencies and conflicts, and plan skill installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can make persistent skill installs from ClawHub without pinning or verifying the resolved versions.

Mitigation: Review the dependency plan before installation, prefer manually pinned installs, and do not treat auto-resolution output as an integrity guarantee.

Risk: Dependency and conflict results depend on local skill metadata and the configured OpenClaw skill directories.

Mitigation: Review the scanned directories and skill metadata before acting on missing-dependency or conflict reports.

## Reference(s):

- [ClawHub Skill Dependencies page](https://clawhub.ai/myrodar/skills/skill-deps)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts inspect local OpenClaw skill directories and may query ClawHub when searching or resolving installs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
