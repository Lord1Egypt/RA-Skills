## Description:

Analyzes nighttime bedroom audio and video for observable sleep events such as sudden sitting, shouting, and arm movements, then summarizes their timing and frequency for caregivers and clinical review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Family caregivers and care staff can review summaries of nighttime audio and video for observable sleep events and share the event record with a clinician. Results are monitoring information for clinical review, not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bedroom sleep video and identity or account data may be sent to or stored by a remote service.

Mitigation: Before use, verify the video-processing destination and terms, determine what identity and account data are sent or stored, and confirm export-only behavior. Obtain the older adult's informed consent and protect any retained data.

Risk: Caregivers may mistake detected behavior patterns for a medical diagnosis.

Mitigation: Treat the results as observations for a clinician to review; do not use them to diagnose a condition or adjust medication.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-elderly-nightmare-startle-detect-analysis)
- [API reference](artifact/references/api_doc.md)
- [Skill introduction](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Structured event summaries in JSON or text; history lists in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include event timing, counts, duration, summaries, recommendations, and report links; outputs are not medical diagnoses.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
