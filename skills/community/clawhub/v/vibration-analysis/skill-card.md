## Description:

Analyzes wind turbine drivetrain vibration data from CMS trends, RMS/peak values, frequency spectrum, and SCADA alarms, then classifies severity and recommends monitoring or shutdown actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sertug17](https://clawhub.ai/user/sertug17)

### License/Terms of Use:

MIT

## Use Case:

External developers, wind operations teams, and maintenance engineers use this skill to assess wind turbine drivetrain vibration health, interpret CMS/SCADA indicators, classify component severity, and prepare a diagnostic report with recommended next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wind turbine shutdown or continued-operation recommendations could be treated as operational authority without qualified review.

Mitigation: Validate severity, shutdown posture, maintenance timing, and data quality with qualified site personnel against OEM guidance, site procedures, recent maintenance records, and live operating conditions.

Risk: Vibration findings can be misleading when CMS/SCADA inputs lack RPM-normalized spectrum data, site baselines, or operating context.

Mitigation: Require RPM-normalized spectrum data where spectral diagnosis is used, compare values against site-specific baselines, and cross-check alarms with recent weather, grid, load, and maintenance events.

## Reference(s):

- [Vibration Analysis skill page](https://clawhub.ai/sertug17/skills/vibration-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown diagnostic report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes drivetrain severity, shutdown posture, fault hypotheses, recommended actions, escalation triggers, and verification questions.]

## Skill Version(s):

1.0.0 (source: release evidence, target metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
