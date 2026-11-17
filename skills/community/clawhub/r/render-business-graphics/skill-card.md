## Description:

Turns structured business content into organization charts, flows, schedules, timelines, and data visualizations as SVG or PNG images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zslzxy](https://clawhub.ai/user/zslzxy)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and developers use the skill to turn structured business information into diagrams and charts for reports, project plans, and system designs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential chart data may be sent to an external rendering service.

Mitigation: Review the configured service address and avoid sending sensitive data until the service is trusted.

Risk: An unintended service address or API key may expose business data or credentials.

Mitigation: Set CHART_RENDER_BASE_URL and CHART_RENDER_API_KEY deliberately and use non-sensitive test data first.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zslzxy/skills/render-business-graphics)
- [Graphics selection and themes](artifact/references/selection-and-themes.md)
- [Graphic types and examples](artifact/references/graphics/index.md)
- [Rendering API documentation](artifact/references/http-api.md)

## Skill Output:

**Output Type(s):** [SVG images, PNG images, JSON render requests, Guidance]

**Output Format:** [SVG or PNG image files with structured JSON requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Images are saved locally; optional render metadata is available as JSON.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
