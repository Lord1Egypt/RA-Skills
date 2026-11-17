## Description:

Analyzes aquarium video for fish surface gasping and abnormal breathing, then provides visual risk alerts and suggested water-quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarium owners, aquarium staff, and aquaculture operators can use video analysis to flag fish surface gasping or abnormal breathing and decide when to check water conditions. Results are visual risk warnings, not a confirmed diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags suspicious account, data, and remote-service behavior, including a reported risk that a configured secret may be sent during registration.

Mitigation: Review registration, credential handling, remote destinations, and host permissions before use; provide only an appropriately scoped secret after verifying its handling.

Risk: Video analysis and historical report access involve remote processing and account or identity handling, which may affect the privacy of aquarium footage and report data.

Mitigation: Use only footage and account data authorized for remote processing, and confirm retention, access, and export practices meet your requirements before uploading or sharing reports.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-fish-gasping-ammonia-warning-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured analysis report or text summary with visual risk alerts, observations, suggested checks, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video-based observations; does not confirm water chemistry or diagnose disease.]

## Skill Version(s):

1.0.19 (source: server-resolved release evidence; artifact SKILL.md frontmatter lists 1.0.21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
