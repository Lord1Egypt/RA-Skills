## Description: <br>
Analyzes wind turbine drivetrain vibration data from CMS trends, RMS and peak values, frequency spectrum, and SCADA alarms to classify severity and recommend shutdown or monitoring actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sertug17](https://clawhub.ai/user/Sertug17) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Wind operations, maintenance, and reliability teams use this skill to assess CMS and SCADA vibration evidence, classify drivetrain severity, and decide whether to monitor, inspect, plan shutdown, or shut down immediately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Severity scores and shutdown recommendations could be mistaken for automatic operational authority. <br>
Mitigation: Treat the output as decision support and confirm results against OEM guidance, current operating conditions, and qualified engineering review before operational action. <br>
Risk: Generic vibration thresholds may not match site-specific baselines or recent maintenance context. <br>
Mitigation: Validate findings against site-specific CMS baselines, RPM-normalized spectrum data, SCADA events, and recent maintenance history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sertug17/vibration-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes missing data notes, component-level severity, drivetrain severity, shutdown recommendation, fault hypotheses, recommended actions, and escalation triggers.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
