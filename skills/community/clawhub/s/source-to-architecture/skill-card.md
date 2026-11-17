## Description:

Generates five-layer architecture visualizations and analysis artifacts from source code structure, dependencies, and module mappings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architects use this skill to scan a project, map modules into access, routing/control, logic, data access, and storage/external layers, and generate architecture diagrams for review or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and workflow steps can make broad local changes, including global tool installation, sudo-based package installation, and Dockerfile creation.

Mitigation: Review installer commands first, run in a disposable or containerized environment where possible, avoid sudo or global installs, and back up any existing Dockerfile.

Risk: Project scanning and synchronization workflows may inspect or modify more of the local workspace than intended.

Mitigation: Explicitly limit scanned project directories and review any Git hooks, scheduled synchronization, or generated change reports before enabling them.

## Reference(s):

- [Source To Architecture ClawHub page](https://clawhub.ai/vincentlau2046-sudo/skills/source-to-architecture)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON analysis files, and DrawIO architecture files with optional PNG, SVG, or PDF exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces source analysis, dependency and mapping summaries, and five-layer architecture diagrams for agent-assisted documentation workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
