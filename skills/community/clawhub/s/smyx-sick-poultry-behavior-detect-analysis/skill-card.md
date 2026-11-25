## Description:

Analyzes poultry and pig barn images or videos for abnormal behavior cues and returns behavior types and risk levels for early screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock producers and farm operators use this skill to screen barn footage for abnormal individual or group behavior and review risk-ranked reports. Results are for early screening; the skill does not provide disease diagnoses or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags account and token handling beyond the skill’s stated livestock video analysis purpose.

Mitigation: Review the security findings and account behavior before use, and avoid supplying credentials unless you trust the skill and its service.

Risk: The security evidence flags possible remote media analysis, which may send barn images or video to an external service.

Mitigation: Use only footage you are authorized to share, and avoid uploading sensitive media until the destination and handling are understood.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-sick-poultry-behavior-detect-analysis)
- [API interface reference](artifact/references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured analysis report in JSON or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include observed behavior cues, animal or group location, risk level, group abnormality proportion, and a report link; screening results are not a diagnosis.]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
