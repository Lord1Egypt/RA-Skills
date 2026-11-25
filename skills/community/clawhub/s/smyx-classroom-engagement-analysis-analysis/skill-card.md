## Description:

Using a fixed classroom camera, the system analyzes students' facial expressions (focused, confused, happy, frustrated, bored, etc.), computes a class-level overall engagement score (0-100), and can identify low-engagement student positions (no identity stored — for real-time teacher reminders only).

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and education staff use classroom video to review class-level engagement patterns, identify seat positions that may need attention, and receive suggestions for adjusting teaching. The skill is intended for classroom and training settings where students are on camera.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious and flags unclear video submission and consent practices.

Mitigation: Before use, verify where classroom video is sent and how consent is obtained.

Risk: The security review flags account registration and token storage that are not clearly disclosed.

Mitigation: Before use, verify the account creation and token storage behavior.

Risk: The security review says video analysis may still occur when export-only mode is requested.

Mitigation: Do not rely on export-only mode until you have verified that it prevents analysis.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-classroom-engagement-analysis-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Image]

**Output Format:** [Structured analysis report in JSON or Markdown, with an engagement score, anonymized seat-position observations, recommendations, and a report link; heatmap image where supported.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include emotion classifications and anonymous seat-grid coordinates derived from classroom video.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata; artifact frontmatter lists 1.0.22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
