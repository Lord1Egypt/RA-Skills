## Description:

Analyzes video of a water-cup area to count cup pickups as an indirect measure of drinking frequency and flag counts below a preset threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Family caregivers and elder-care staff can use this skill to review video from a fixed camera aimed at a cup area, track pickup frequency, and receive low-frequency reminders. Pickup counts are only an indirect proxy for water intake and are not a clinical assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious because it reports remote account registration and video submission; the scan was partial.

Mitigation: Do not install until the remote service, identity data sent, video-processing behavior, and export-only behavior are explained and reviewed.

Risk: Camera footage may include identifiable people in private homes or care settings.

Mitigation: Obtain informed consent before use and handle footage securely, as the skill documentation advises.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration page](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Structured drinking-frequency report in JSON or a Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pickup counts are an indirect proxy for water intake; camera coverage and shared-cup use can affect counts.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata; embedded SKILL.md frontmatter states 1.0.21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
