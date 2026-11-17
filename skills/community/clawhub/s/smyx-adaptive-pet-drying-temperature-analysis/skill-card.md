## Description:

Analyzes pet images or videos to estimate breed or body type and coat density, then recommends a drying temperature and duration curve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Pet groomers and smart pet-care device operators use the skill to obtain drying temperature and duration guidance from pet images or videos and to retrieve previous reports. Recommendations are for grooming, not medical care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet media or supplied URLs are sent to lifeemergence.com services for processing.

Mitigation: Review and approve remote processing before use; share only pet media and URLs authorized for upload.

Risk: The skill can create or reuse an account identifier and store authentication tokens in the workspace data directory.

Mitigation: Review account linkage and local token storage before installation; restrict access to the workspace data directory.

Risk: Broad history-related prompts can trigger queries of cloud-stored reports.

Mitigation: Confirm intent and authorization before querying or sharing previous reports.

Risk: Automated temperature recommendations may be unsuitable for a particular pet.

Mitigation: Treat recommendations as grooming guidance, not medical advice; monitor the pet and verify device settings before use.

## Reference(s):

- [Skill API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release](https://clawhub.ai/18072937735/skills/smyx-adaptive-pet-drying-temperature-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured analysis report or Markdown history table; optional JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes recommended drying temperatures (°C), durations (minutes), and report links when available.]

## Skill Version(s):

1.0.13 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
