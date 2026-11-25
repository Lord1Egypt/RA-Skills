## Description:

Analyzes images and videos to monitor personnel presence in designated areas, flag possible absences, and produce structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams use this skill to review workplace images or videos for personnel presence in designated areas and generate absence monitoring reports. It can also retrieve prior report listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible unintended remote data transfers, including uncertainty about where video and identity data are sent.

Mitigation: Verify the destination and handling of videos, identity data, and credentials before use; avoid sending sensitive footage until those details are clear.

Risk: The security review flags actions that may exceed the stated purpose and unclear side effects, including uncertainty about export-only behavior.

Mitigation: Confirm that actions and side effects match the monitoring task, and verify that export-only mode does not perform analysis before relying on it.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release](https://clawhub.ai/18072937735/skills/smyx-staff-absence-detection-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured JSON reports and Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
