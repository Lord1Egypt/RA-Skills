## Description:

Analyzes video of an older adult's resting hand to estimate tremor frequency and amplitude and flag possible resting tremor for screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Family caregivers and care providers can use resting-hand video analysis as an early screening aid to observe tremor indicators and decide when to seek professional medical review. The results are video-based indicators, not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags undisclosed account registration, credential storage, user lookup, and remote handling; health video is sensitive information.

Mitigation: Before use, verify the account and data handling behavior, obtain consent for any video processing, and avoid uploading sensitive video until the data flow is understood.

Risk: The security assessment reports that health video may be processed despite an export-only option; the assessment is partial and does not establish that video is sent to the account endpoint or that the author acted maliciously.

Mitigation: Review the relevant behavior and test with non-sensitive sample video before relying on export-only settings or processing real recordings.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-elderly-hand-tremor-detection-analysis)
- [Skill introduction](https://lifeemergence.com/sample.html)
- [API documentation](references/api_doc.md)
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report with tremor metrics, affected side, risk level, and report link when available; Markdown for history listings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tremor frequency (Hz), pixel displacement amplitude, rhythm consistency, and a screening risk level; results are not a clinical diagnosis.]

## Skill Version(s):

1.0.18 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
