## Description:

修复损坏的 Python venv 与缺标准库模块（_sqlite3）导致的服务启动失败。

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterliu-512](https://clawhub.ai/user/peterliu-512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to diagnose broken Python virtual environments, missing standard-library C extensions, and service startup failures on Linux systems. It guides repair choices such as ABI-compatible module replacement or virtual environment rebuilds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The repair workflow can make privileged, persistent changes under /usr/local.

Mitigation: Confirm package provenance, ABI compatibility, destination files, backups, and rollback steps before copying system Python extension files.

Risk: The virtual environment rebuild path may delete the wrong directory if the venv path is incorrect.

Mitigation: Verify the exact absolute path and prefer renaming the old virtual environment to a backup before using rm -rf.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/peterliu-512/skills/python-venv-repair)
- [Publisher Profile](https://clawhub.ai/user/peterliu-512)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
