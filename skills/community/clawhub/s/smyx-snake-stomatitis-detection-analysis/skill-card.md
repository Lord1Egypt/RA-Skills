## Description:

Submits snake mouth images, videos, or URLs for cloud-based stomatitis-risk analysis and returns reports with suggested follow-up actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Snake keepers, breeders, and reptile-care professionals can submit mouth images or videos for a preliminary stomatitis-risk report and retrieve earlier reports. The results are not a veterinary diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snake images, videos, or URLs are submitted to LifeEmergence cloud services.

Mitigation: Review media handling, retention, deletion, and account linkage with the publisher before use.

Risk: The skill creates or reuses an account and persists session tokens in a local workspace database.

Mitigation: Restrict access to the workspace and review token storage and cleanup before installing.

Risk: A visual risk assessment could be mistaken for a veterinary diagnosis.

Mitigation: Treat reports as screening information only and consult a reptile veterinarian for diagnosis and treatment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-snake-stomatitis-detection-analysis)
- [API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured risk report or Markdown table with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports historical report lookup and optional file export.]

## Skill Version(s):

1.0.13 (source: server-resolved ClawHub release; bundled frontmatter says 1.0.18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
