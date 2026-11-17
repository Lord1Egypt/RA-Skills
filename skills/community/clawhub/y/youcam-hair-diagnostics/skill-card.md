## Description:

Analyzes selected hair density, type, frizziness, and length metrics from user-provided photos and returns a combined report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcam-api](https://clawhub.ai/user/youcam-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can choose hair density, type, frizziness, or length analysis to get a combined hair-health overview with plain-language notes and gentle care suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected photos are sent to YouCam/Perfect Corp for analysis.

Mitigation: Disclose the upload and review the provider's retention terms before sharing photos.

Risk: API calls consume credits, and type and frizziness analysis require three angles.

Mitigation: Check the cost of each selected metric and get the user's choice before running; request front, right, and left views for type or frizziness.

Risk: The API key must be protected; installed dependency versions and provider retention were not verified.

Mitigation: Store the key in the environment or local credentials file, review retention terms, and keep dependencies updated.

## Reference(s):

- [Hair diagnostics interpretation guide](references/guide.md)
- [YouCam Hair Density Detection API](https://docs.perfectcorp.com/reference/ai_hair_density_detection.md)
- [YouCam Hair Type Detection API](https://docs.perfectcorp.com/reference/ai_hair_type_detection.md)
- [YouCam Hair Frizziness Detection API](https://docs.perfectcorp.com/reference/ai_hair_frizziness_detection.md)
- [YouCam Hair Length Detection API](https://docs.perfectcorp.com/reference/ai_hair_length_detection.md)
- [YouCam API Console](https://yce.perfectcorp.com/api-console)
- [ClawHub release](https://clawhub.ai/youcam-api/skills/youcam-hair-diagnostics)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with selected metrics, plain-language notes, an overall summary, and gentle care suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only metrics returned by the API; results are for reference and are not a medical diagnosis.]

## Skill Version(s):

1.1.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
