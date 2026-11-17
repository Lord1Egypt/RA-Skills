## Description:

Analyzes images and short videos for possible falls and provides reports for home care and nursing-home safety monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and families use images or short video clips to check for possible falls and review past analysis reports. Results are safety guidance, not a substitute for human confirmation or emergency response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, videos, URLs, and report history may be sent to lifeemergence.com services.

Mitigation: Share only footage approved for this service; avoid highly sensitive care footage until retention, deletion, and authorization practices are documented.

Risk: The skill handles identity and remote login and can store identity and tokens in a local workspace database.

Mitigation: Review the publisher's identity and token storage practices before installing and restrict access to the local workspace.

Risk: Fall-detection results may be mistaken for a confirmed emergency assessment.

Mitigation: Confirm suspected falls with a person and follow appropriate emergency procedures.

## Reference(s):

- [Fall detection API documentation](references/api_doc.md)
- [Analysis API error codes](skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release listing](https://clawhub.ai/18072937735/skills/smyx-fall-detection-image-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Structured fall-detection report or Markdown history table; JSON output is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk feedback, recommendations, and report links; reports can be saved to a file]

## Skill Version(s):

1.0.17 (source: ClawHub release metadata; SKILL.md frontmatter lists 1.0.15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
