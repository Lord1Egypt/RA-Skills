## Description:

Analyzes outdoor surveillance images and videos to detect people, vehicles, non-motorized vehicles, and pets, and produces monitoring reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External users managing courtyards, orchards, farms, and other outdoor areas can submit images or videos for object detection, intrusion assessment, and monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Surveillance media and identity data may be sent to remote services or associated with account and report records.

Mitigation: Before submitting media, clarify the destination, account handling, access, and retention practices; avoid sharing sensitive footage unless approved.

Risk: The scanner reports that the export-only option may still analyze supplied media.

Mitigation: Do not rely on that option to prevent analysis; clarify its behavior and avoid supplying sensitive media until confirmed.

Risk: The security scan was partial because a referenced local path was missing, so it may not cover the complete skill package.

Mitigation: Review the missing component and complete a full package security review before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/18072937735/skills/smyx-outdoor-monitoring-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API interface documentation](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured monitoring reports with detection results, counts, risk notes, recommendations, and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts JPG, JPEG, PNG, MP4, AVI, and MOV files up to 10 MB; results are for security reference only.]

## Skill Version(s):

1.0.22 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
