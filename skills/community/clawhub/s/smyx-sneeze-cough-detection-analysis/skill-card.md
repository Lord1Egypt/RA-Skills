## Description:

Analyzes pet videos, optionally using audio, to identify sneeze and cough events and report their timing and frequency; results are for behavior observation, not medical diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, veterinary clinic staff, and boarding center operators can use the skill to review pet activity videos for sneeze and cough events, their frequency, and related behavior observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked this release suspicious for undisclosed account and credential handling, external media processing without clear notice, and behavior that may not fully match the stated purpose. The scan was partial because a referenced local path was missing.

Mitigation: Review the security assessment and the missing-path coverage before installing. Use an isolated account and avoid sending sensitive footage until identity and token handling, media processing, and retention are understood.

Risk: Pet videos may be processed by an external service, and automated behavior observations are not a veterinary diagnosis.

Mitigation: Submit only footage you are authorized to share, and consult a veterinarian about frequent, persistent, or urgent symptoms.

## Reference(s):

- [API documentation](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-sneeze-cough-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured text or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports event types, timing, frequency, observations, and report links; can also list prior reports.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
