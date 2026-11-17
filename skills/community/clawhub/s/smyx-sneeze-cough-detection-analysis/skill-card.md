## Description:

Analyzes pet video, with optional audio, for sneeze and cough behaviors and returns event summaries and report history for observation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners, veterinary staff, and boarding staff can review pet videos for sneeze and cough behavior, track event frequency, and retrieve prior reports for observation. Results support monitoring only and do not provide a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags broad remote media processing as a concern that does not clearly match the stated pet-monitoring purpose.

Mitigation: Before submitting a video, audio, or URL, confirm you are comfortable sharing that media with the service and only submit material you are authorized to share.

Risk: The security review says account registration and credential storage are unexpected and unexplained.

Mitigation: Wait to install or use the skill until the publisher explains why identity registration and credential storage are needed and how credentials are handled.

Risk: The security review is incomplete because a local reference could not be resolved and some imported behavior could not be assessed.

Mitigation: Resolve the missing reference and review the unassessed imported behavior before relying on the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-sneeze-cough-detection-analysis)
- [Skill introduction](https://lifeemergence.com/sample.html)
- [API reference](references/api_doc.md)
- [Analysis API reference](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [JSON or Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include behavior labels, event times and frequency, suggestions, and report links; results are for observation, not medical diagnosis.]

## Skill Version(s):

1.0.16 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
