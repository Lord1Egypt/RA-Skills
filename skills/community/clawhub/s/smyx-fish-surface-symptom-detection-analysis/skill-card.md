## Description:

Analyzes fish images or video for visible signs of white spots, hyperemia, or fin rot and returns a confidence-rated report for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarists and aquarium operators can use the skill to review fish images or video for visible surface symptoms and receive a structured report with confidence, location, severity, and suggested next steps. The results are visual indicators and do not replace diagnosis by an aquatic veterinarian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports account and credential handling and persistent user data.

Mitigation: Review what account information, credentials, and user data are handled before use, and provide only information required for the task.

Risk: The security summary says an export-only option may still trigger remote analysis and flags remote media processing.

Mitigation: Do not rely on export-only mode as a privacy boundary; confirm whether images or video will be sent for remote analysis before using sensitive media.

Risk: The security scan is partial because a local reference could not be resolved, leaving the evidence incomplete.

Mitigation: Resolve the missing reference and review the resulting security evidence before relying on the scan as complete.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis report, JSON, Text, Markdown, Guidance]

**Output Format:** [Structured JSON or text report; history results can be presented as a Markdown list or table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include symptom labels, confidence, location, severity, suggested actions, and report links when available. Results are visual indicators, not veterinary diagnoses.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
