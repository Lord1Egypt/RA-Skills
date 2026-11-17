## Description:

Traffic Monitor helps agents check server network usage for a configured interface, generate monthly traffic reports, and warn when usage crosses an 80% threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binyuli](https://clawhub.ai/user/binyuli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and server operators use this skill to inspect vnstat-based monthly, daily, and live network traffic for a server interface. It is especially suited to monitoring a configured 2 TB monthly traffic limit and surfacing warnings before overage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Traffic reports may be incorrect if the server does not use the configured interface name or monthly traffic limit.

Mitigation: Review and adjust the interface name and monthly limit before relying on usage reports or alerts.

Risk: Administrative service commands can affect traffic collection if run without review.

Mitigation: Treat systemctl examples as manual administrative actions and run them only after confirming the intended service state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binyuli/skills/traffic-monitor)
- [Publisher profile](https://clawhub.ai/user/binyuli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and human-readable text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports depend on vnstat data for the configured network interface and threshold settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
