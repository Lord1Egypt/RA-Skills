## Description:

Assesses ornamental fish coloration from images or video and reports a vibrancy score against species-specific color ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Aquarium keepers, aquaculture operators, and developers can use the skill to assess fish coloration from a suitable image or video and review a structured report with color trends and husbandry suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account identity and credential handling warrant review before use.

Mitigation: Review how identity and credentials are handled, and use only the access needed for the analysis.

Risk: The local-media upload and data-handling behavior is not clearly disclosed.

Mitigation: Before submitting fish images or videos, verify where they are sent and how they are retained; obtain the aquarium owner's consent where applicable.

Risk: The reported behavior may be limited to exporting analysis results.

Mitigation: Treat scores and reports as informational, check results against the fish and capture conditions, and do not use them as a diagnosis or to trigger equipment changes automatically.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-color-brightness-assessment-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text, Guidance]

**Output Format:** [Structured JSON report or text summary, with report links when supplied]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-fish vibrancy score (0–100), color status, species baseline comparison, and optional 7-day and 30-day trends]

## Skill Version(s):

1.0.16 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
