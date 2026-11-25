## Description:

Analyzes camera images and video frames to identify quality issues such as black or white screens, color casts, stripes, noise, and blur.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams use the skill to check camera images or video frames for visual quality problems during surveillance system maintenance and camera self-checks. They can also request a list of historical analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports undeclared account and token handling and remote transmission of data, including behavior that may analyze or upload media in export-only mode.

Mitigation: Review the destination and identity-handling behavior before use. Do not treat export-only mode as a privacy boundary, and avoid sensitive camera footage until you have confirmed it may be shared with the service.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured analysis report with findings, recommendations, and report links; Markdown table for historical report lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports camera image and video inputs; analysis results are for maintenance reference and do not replace hardware inspection.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
