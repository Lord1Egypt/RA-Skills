## Description:

Help install, configure, run, troubleshoot, and extend MolecularAI REINVENT4 for generative molecular design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoeprior](https://clawhub.ai/user/zoeprior)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational chemistry practitioners use this skill to get REINVENT4-specific guidance for installation, backend selection, TOML configuration, sampling, scoring, transfer learning, staged learning, notebook conversion, plugin work, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated install or runtime commands may target the wrong checkout, environment, backend, or dependency set.

Mitigation: Confirm the REINVENT4 checkout markers, use an isolated Python environment, inspect help output, and prefer dry-run installs before executing real install commands.

Risk: Optional licensed or external scoring integrations can fail or create compliance issues when required upstream tools are unavailable.

Mitigation: Enable optional OpenEye, iSIM, docking, REST, or external-process integrations only after confirming the relevant tool, license, and local configuration are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoeprior/skills/reinvent4)
- [Install And Run](references/install-and-run.md)
- [Config Modes](references/config-modes.md)
- [Plugins, Notebooks, And Tests](references/plugins-and-tests.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should keep paths explicit, prefer local checkout verification, and avoid promising complete runs unless required models, data, configs, and licensed tools are present.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
