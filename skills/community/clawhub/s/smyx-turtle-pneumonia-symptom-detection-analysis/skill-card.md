## Description:

Analyzes turtle mouth and nasal videos for frequent open-mouth breathing, mucus, or nasal discharge and returns a pneumonia-risk warning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Turtle keepers and reptile-care teams can use fixed-camera video to flag visible respiratory warning signs and review structured observations. Treat results as visual alerts, not a diagnosis; a reptile veterinarian must confirm disease.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos or video URLs are sent to Life Emergence, and retention and billing terms need review.

Mitigation: Review the service's retention and billing terms before sharing footage. Package retention statements do not demonstrate server-side enforcement.

Risk: The security review flags credential destination checks, and service use can save authentication tokens locally.

Mitigation: Wait for fixes to credential destination checks and protect the local environment where tokens may be saved.

Risk: The export-only option may still allow video processing.

Mitigation: Do not rely on export-only mode to prevent processing; verify behavior before using it with footage.

## Reference(s):

- [ClawHub release](https://clawhub.ai/18072937735/skills/smyx-turtle-pneumonia-symptom-detection-analysis)
- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured text or JSON; Markdown for history listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual warning signs, observations, and suggested follow-up; not a veterinary diagnosis.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
