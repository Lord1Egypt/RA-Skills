## Description:

Analyzes infant-cry audio or audio/video and returns a likely cause, confidence, and directional soothing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers can use the skill to review an infant-cry recording and get a possible cause with a confidence score and soothing hint. Treat the result as a parenting aid, not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is suspicious: it reports undeclared account provisioning, persistent identity and token storage, possible recording uploads, and that infant-specific analysis is not demonstrated; coverage was partial.

Mitigation: Avoid installation until the behavior and data handling are clarified.

Risk: Infant audio is sensitive personal data, and the assessment reports possible recording uploads.

Mitigation: Obtain guardian consent and clarify recording upload, storage, and retention before using infant recordings.

Risk: A cry-cause classification can be mistaken for a medical assessment.

Mitigation: Use results only as a parenting reference; seek medical care for persistent or concerning symptoms.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-infant-cry-cause-classification-analysis)
- [Publisher profile](https://clawhub.ai/user/18072937735)
- [API reference](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured JSON analysis with a report export link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a likely cause, confidence, secondary causes, audio-feature summary, and directional soothing hint; not a medical diagnosis.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
