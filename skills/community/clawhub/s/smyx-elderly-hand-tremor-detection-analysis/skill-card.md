## Description:

Analyzes video of a resting hand to estimate tremor frequency and amplitude and provide a screening risk indication; it does not diagnose medical conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Family caregivers and care staff can use a video of an older adult's resting hand to review estimated tremor measurements and screening indications. The results can prompt follow-up with a healthcare professional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports remote processing of sensitive hand video and unclear identity or account handling.

Mitigation: Obtain informed consent and use the service only if you are comfortable with the reported data processing.

Risk: The security scan reports that processing may continue despite an export-only request.

Mitigation: Confirm the intended operation before running the skill and review any upload or processing action.

Risk: Security guidance flags local credential storage.

Mitigation: Protect the device and restrict access to locally stored credentials.

Risk: Video-based tremor estimates could be mistaken for a clinical diagnosis.

Mitigation: Treat results as screening information only and consult a qualified healthcare professional for assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-elderly-hand-tremor-detection-analysis)
- [API interface reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [Structured analysis report with tremor measurements, screening risk indication, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video-derived estimates and screening prompts; not a clinical diagnosis.]

## Skill Version(s):

1.0.17 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
