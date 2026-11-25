## Description:

Using a fixed camera in the living room or kitchen, the system analyzes video of the water-cup placement area (e.g., coffee table, dining table), detects hand-to-cup contact actions (pickup, putdown), and counts daily cup-pickup events (an indirect proxy for water intake).

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Families, caregivers, and care facilities use the skill to analyze fixed-camera footage around a water-cup area, count cup pickup events as an indirect indicator of drinking frequency, and receive prompts when counts are low. It provides behavioral summaries and directional reminders rather than medical diagnoses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reported video upload, account registration, identity transmission, and workspace-token storage may expose sensitive recordings or account data during remote processing.

Mitigation: Use only recordings with informed consent; review service destinations and token handling before use, and avoid sensitive footage or account details unless needed.

Risk: The security scan was partial because one local reference could not be resolved, so not every referenced resource was assessed.

Mitigation: Resolve and review the missing reference before deployment, and do not treat the scan as exhaustive.

Risk: A configuration-only flag does not prevent analysis.

Mitigation: Confirm the actual processing controls before relying on configuration settings to suppress analysis.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-elderly-drinking-frequency-analysis)

## Skill Output:

**Output Type(s):** [Analysis reports, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report (JSON); historical report lists may be presented as Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cup pickup counts are an indirect proxy for drinking behavior and do not establish actual water intake or diagnose a medical condition.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
