## Description:

Manages scheduled intraday A-share stock monitoring tasks, including market updates, deeper analysis, pre-close analysis, and task start, stop, and frequency changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cle87937-code](https://clawhub.ai/user/cle87937-code)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill to configure and manage automated A-share trading-session monitoring schedules, with reports sent to a configured channel. It is suited for recurring market checks, configurable analysis depth, and pre-close decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends weakening command-execution security globally.

Mitigation: Prefer least-privilege allowlist entries and do not set tools.exec.security to full globally unless the operator has explicitly accepted that risk.

Risk: The skill asks users to run PowerShell setup and management scripts that are not included in the artifact.

Mitigation: Run setup.ps1 or manage.ps1 only after obtaining them from a trusted source and inspecting or verifying them first.

Risk: Scheduled stock-monitoring tasks can repeatedly generate trading guidance during market hours.

Mitigation: Review scheduled messages and trading advice before acting on them, and install only if the scheduling behavior is understood and accepted.

## Reference(s):

- [trading-monitor configuration guide](references/config-guide.md)
- [ClawHub skill page](https://clawhub.ai/cle87937-code/skills/trading-monitor)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with PowerShell and OpenClaw command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scheduled monitoring setup and management guidance; no fixed machine-readable output contract is documented.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
