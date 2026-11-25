## Description:

Analyzes images and videos to identify movement patterns such as tremors, convulsions, stiffness, and gait abnormalities for home monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and care teams can use the skill to review patient images or videos for movement patterns associated with Parkinson's disease or epileptic episodes and receive monitoring reports. Results are for auxiliary monitoring and do not replace a medical diagnosis or a clinician's judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with high confidence and cites concerns about identity sharing, credential handling, and behavior that may not match its video-monitoring purpose.

Mitigation: Review the security findings and configuration before installation or execution, and protect credentials and internal identity values.

Risk: Patient recordings are sensitive and may be processed unexpectedly; scanner evidence is incomplete and some interpretations are disputed.

Mitigation: Use only recordings you are authorized to share, review how recordings and reports are handled, and treat results as monitoring aids rather than diagnoses.

## Reference(s):

- [API interface reference](references/api_doc.md)
- [API errors and response details](skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured analysis reports and report summaries, with recommendations and report links where available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis reports may include monitoring findings; historical report lists are presented as Markdown tables.]

## Skill Version(s):

1.0.17 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
