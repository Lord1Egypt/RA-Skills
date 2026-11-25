## Description:

Analyzes elderly sleep video and audio for unusual movements or sounds, then summarizes event timing, frequency, and duration for caregiver review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Family caregivers and care staff use this skill to review overnight sleep recordings for unusual events and prepare summaries for discussion with a clinician. The results describe observed behavior and are not a medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the release suspicious and reports unclear credential handling and automatic account registration.

Mitigation: Ask the publisher to clarify these behaviors and review them before installation; do not provide production credentials until they are understood.

Risk: Disclosure and authorization for sensitive sleep recordings are unclear.

Mitigation: Obtain consent and confirm how recordings are submitted, accessed, and retained before using the skill with real footage.

Risk: The security review flags export-only behavior as needing clarification, and the scan was partial because a local reference was missing.

Mitigation: Clarify and review the export-only behavior and the missing reference before relying on the scan or using the release.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-elderly-nightmare-startle-detect-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API interface notes](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text, Guidance]

**Output Format:** [Structured event report in JSON or readable text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Event timeline, counts, durations, and caregiver-facing summary; not a medical diagnosis.]

## Skill Version(s):

1.0.17 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
