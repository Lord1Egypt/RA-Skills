## Description:

Taichi is a multi-agent collaboration framework that supports centralized, distributed, and hybrid execution modes through a Redis message bus and Planner, Drafter, Validator, and Dispatcher workflow stages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indivisible2025](https://clawhub.ai/user/indivisible2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Taichi to run multi-agent workflows for linear task planning, parallel data processing, and multi-stage task coordination across centralized, distributed, or hybrid execution modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The framework includes unsafe shell execution behavior that can run local commands.

Mitigation: Review and patch the subprocess executor before using real data, and restrict execution to explicitly approved commands.

Risk: Install and uninstall scripts can make broad local environment changes, including host package installation and workspace deletion.

Mitigation: Install only in an isolated development environment, avoid sudo unless host package changes are intended, and keep TAICHI_WORKSPACE scoped to the framework workspace.

Risk: The workflow depends on Redis for inter-agent messaging.

Mitigation: Use a local, protected Redis instance and avoid exposing the message bus to untrusted networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indivisible2025/skills/taichi)
- [Project homepage](https://github.com/Indivisible2025/Cloudfin)
- [Taichi framework README](artifact/taichi-framework/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and runtime text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+, a Python virtual environment, and a local Redis message bus.]

## Skill Version(s):

2.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
