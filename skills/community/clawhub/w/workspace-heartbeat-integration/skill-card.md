## Description:

Synchronizes workspace heartbeat state with memory logs and generates heartbeat reports for ongoing work tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate recurring workspace heartbeat checks, append structured work-session logs, synchronize heartbeat state, and produce status reports from workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can publish the package using the user's ClawHub credentials without a separate approval step.

Mitigation: Review install.sh before installation and remove or disable the clawhub publish command unless publishing this package is intentional.

Risk: The skill persists heartbeat state, daily work logs, and configuration in workspace paths.

Mitigation: Back up existing workspace-heartbeat-integration configuration and memory files, then test with --dry-run or inspect target paths before enabling routine syncs.

## Reference(s):

- [Workspace Heartbeat Integration on ClawHub](https://clawhub.ai/utopiabenben/skills/workspace-heartbeat-integration)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [CLI output, Markdown reports, JSON reports, and workspace memory or configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write heartbeat-state.json, daily memory logs, and config.json in user workspace paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
