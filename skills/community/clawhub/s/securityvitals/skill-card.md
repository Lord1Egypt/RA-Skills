## Description:

Security vitals checker for OpenClaw. Scans your installation, scores your setup, and shows you exactly what to fix. First scan in seconds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bk-cm](https://clawhub.ai/user/bk-cm)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and administrators use SecurityVitals to run point-in-time local security health checks of self-hosted OpenClaw installations, score stable controls, surface experimental notes, and get remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local OpenClaw diagnostic commands, so results depend on the local installation state and command output quality.

Mitigation: Review the requested scan before execution and treat findings as point-in-time diagnostics that may need local confirmation.

Risk: The update status check may indirectly contact the OpenClaw update registry through the OpenClaw CLI.

Mitigation: Skip the update status command when a fully offline scan is required; version-related controls may then be reported as unavailable.

Risk: Reports include optional links to the ClawVitals plugin and dashboard.

Mitigation: Treat those links as optional external resources and verify remediation actions against local policy.

## Reference(s):

- [SecurityVitals ClawHub Listing](https://clawhub.ai/bk-cm/skills/securityvitals)
- [ClawVitals Website](https://clawvitals.io)
- [ClawVitals Documentation](https://clawvitals.io/docs)
- [ClawVitals Controls](https://clawvitals.io/docs/controls)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown security report with command snippets and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Point-in-time report only; no scan history is stored by the skill.]

## Skill Version(s):

1.4.8 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
